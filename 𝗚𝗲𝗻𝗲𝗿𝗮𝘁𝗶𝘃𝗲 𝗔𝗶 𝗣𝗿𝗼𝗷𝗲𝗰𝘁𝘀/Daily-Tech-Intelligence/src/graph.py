"""
The pipeline as a LangGraph state machine.

    START → prepare → write → audit → critic → ┬→ brief → assemble → END
                       ↑                        │
                       └──── revise ←───────────┘   (only if the critic
                                                     rejects a section)

Patterns used (all mirror the workflows in the AI and Data Science repo):
  * sequential chaining        (prepare → write → audit)
  * parallel fan-out           (sections written concurrently)
  * iterative loop             (critic → revise → critic, max N times)
  * conditional routing        (route_after_critic)
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph

from . import prompts
from .config import (
    CRITIC_MODEL,
    GROQ_MODEL,
    LLM_CONCURRENCY,
    LLM_MAX_TOKENS,
    LLM_TIMEOUT,
    MAX_REVISIONS,
    MAX_STORIES_PER_SECTION,
    NEWS_WINDOW_DAYS,
    REASONING_EFFORT,
    SECTIONS,
    SECTION_BY_ID,
)
from .ingest import gather
from .normalize import prepare
from .render import assemble_report
from .schemas import Candidate, LearningPack, SectionReview, today_human
from .tools import audit_section, build_source_index

Progress = Callable[[str, float], None]

_SEM = threading.Semaphore(max(1, LLM_CONCURRENCY))


# --------------------------------------------------------------------------
# State
# --------------------------------------------------------------------------
class BriefState(TypedDict, total=False):
    progress: Progress
    days: int
    max_stories: int
    section_ids: list[str]
    candidates: list[Candidate]
    routed: dict[str, list[Candidate]]
    sections: dict[str, str]
    audits: dict[str, dict]
    reviews: dict[str, dict]
    revisions: int
    brief: str
    learning: dict[str, Any]
    report: str
    log: list[str]


# --------------------------------------------------------------------------
# LLM helpers
# --------------------------------------------------------------------------
def _require_keys() -> None:
    missing = [k for k in ("GROQ_API_KEY", "TAVILY_API_KEY") if not os.getenv(k, "").strip()]
    if missing:
        raise RuntimeError(
            "Missing API key(s): " + ", ".join(missing) + ". "
            "Add them to the .env file in the project root."
        )


def _llm(model: str | None = None, temperature: float = 0.2, max_tokens: int | None = None):
    from langchain_groq import ChatGroq

    name = model or GROQ_MODEL
    kwargs: dict[str, Any] = {}
    # Only reasoning-capable models accept this flag.
    if any(tag in name.lower() for tag in ("gpt-oss", "qwen3", "deepseek")):
        kwargs["reasoning_effort"] = REASONING_EFFORT

    # A stalled HTTP connection must never hang the briefing. We do our own
    # retries, so the client's own retry loop is disabled.
    common: dict[str, Any] = {
        "model": name,
        "api_key": os.getenv("GROQ_API_KEY"),
        "temperature": temperature,
        "max_tokens": max_tokens or LLM_MAX_TOKENS,
        "timeout": LLM_TIMEOUT,
        "max_retries": 0,
    }

    try:
        return ChatGroq(**common, **kwargs)
    except Exception:
        # Fall back if the installed langchain-groq is too old for the flag.
        return ChatGroq(**common)


def _invoke(llm, messages, attempts: int = 5) -> str:
    """Call the model with backoff on rate limits and empty answers."""
    last_error: Exception | None = None
    for i in range(attempts):
        try:
            with _SEM:
                response = llm.invoke(messages)
            content = (
                response.content
                if isinstance(response.content, str)
                else str(response.content)
            )
            if content and content.strip():
                return content
            # Reasoning models can burn the whole budget on hidden reasoning.
            last_error = RuntimeError("Model returned an empty response.")
            if i < attempts - 1:
                time.sleep(1.5 * (i + 1))
                continue
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            message = str(exc).lower()
            retryable = any(
                k in message
                for k in (
                    "rate", "429", "too many", "over capacity", "timeout", "empty",
                    "connection", "connect", "getaddrinfo", "network",
                    "unavailable", "ssl", "502", "503", "504",
                )
            )
            if retryable and i < attempts - 1:
                time.sleep(min(2 * (i + 1), 12))
                continue
            raise
    raise RuntimeError(f"LLM call failed: {last_error}")


def _strip_fences(text: str) -> str:
    text = (text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return text.strip()


def _extract_json(text: str) -> dict:
    text = _strip_fences(text)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model output.")
    return json.loads(text[start: end + 1])


# --------------------------------------------------------------------------
# Nodes
# --------------------------------------------------------------------------
def _node_prepare(state: BriefState) -> dict:
    progress = state.get("progress") or (lambda *_: None)
    raw = gather(
        progress=progress,
        days=state.get("days"),
        section_ids=state.get("section_ids"),
    )
    cleaned, routed = prepare(raw, days=state.get("days"))
    active = state.get("section_ids") or [s.id for s in SECTIONS]
    routed = {sid: items for sid, items in routed.items() if sid in active}
    progress(f"Kept {len(cleaned)} unique stories after de-duplication.", 0.58)
    return {"candidates": cleaned, "routed": routed, "revisions": 0, "log": []}


def _active_sections(state: BriefState):
    ids = state.get("section_ids") or [s.id for s in SECTIONS]
    return [SECTION_BY_ID[sid] for sid in ids if sid in SECTION_BY_ID]


def _write_one(
    section_id: str,
    candidates: list[Candidate],
    progress: Progress,
    window: int,
    max_stories: int,
) -> str:
    section = SECTION_BY_ID[section_id]
    if not candidates:
        return (
            f"_No verified developments matched this section within the last "
            f"{window} days._"
        )

    pool = "\n".join(c.to_prompt() for c in candidates)
    user = prompts.WRITER_USER.format(
        title=section.title,
        focus=section.focus,
        today=today_human(),
        window=window,
        max_stories=max_stories,
        pool=pool,
        label=section.label,
    )
    draft = _invoke(
        _llm(temperature=0.25),
        [SystemMessage(content=prompts.WRITER_SYSTEM), HumanMessage(content=user)],
    )
    return _strip_fences(draft)


def _node_write(state: BriefState) -> dict:
    progress = state.get("progress") or (lambda *_: None)
    routed = state.get("routed", {})
    window = state.get("days") or NEWS_WINDOW_DAYS
    max_stories = state.get("max_stories") or MAX_STORIES_PER_SECTION
    sections: dict[str, str] = {}
    active = _active_sections(state)
    total = max(len(active), 1)
    done = 0
    lock = threading.Lock()

    def work(section_id: str) -> tuple[str, str]:
        nonlocal done
        try:
            text = _write_one(
                section_id, routed.get(section_id, []), progress, window, max_stories
            )
        except Exception as exc:  # noqa: BLE001
            text = (
                "_This section could not be generated in this run "
                f"({type(exc).__name__}). Press **Generate** again to retry it._"
            )
        with lock:
            done += 1
            progress(
                f"Wrote {SECTION_BY_ID[section_id].title} ({done}/{total})",
                0.58 + 0.22 * (done / total),
            )
        return section_id, text

    with ThreadPoolExecutor(max_workers=max(1, LLM_CONCURRENCY)) as pool:
        for section_id, text in pool.map(work, [s.id for s in active]):
            sections[section_id] = text

    return {"sections": sections}


def _node_audit(state: BriefState) -> dict:
    progress = state.get("progress") or (lambda *_: None)
    progress("Running deterministic verification (links, sources, claims)…", 0.81)
    routed = state.get("routed", {})
    sections = state.get("sections", {})

    # Union of every routed URL: a story may legitimately be cited from
    # more than one section.
    all_allowed: set[str] = set()
    for items in routed.values():
        all_allowed |= {c.url for c in items}

    def check(section_id: str) -> tuple[str, dict]:
        allowed = {c.url for c in routed.get(section_id, [])} | all_allowed
        source_text = " ".join(
            f"{c.title} {c.snippet}" for c in routed.get(section_id, [])
        )
        return section_id, audit_section(sections.get(section_id, ""), allowed, source_text)

    audits: dict[str, dict] = {}
    if not sections:
        return {"audits": audits}

    with ThreadPoolExecutor(max_workers=min(8, len(sections))) as pool:
        for section_id, result in pool.map(check, list(sections)):
            audits[section_id] = result

    return {"audits": audits}


def _node_critic(state: BriefState) -> dict:
    progress = state.get("progress") or (lambda *_: None)
    progress("Editor agent reviewing accuracy and structure…", 0.86)
    routed = state.get("routed", {})
    reviews: dict[str, dict] = {}

    critic = _llm(model=CRITIC_MODEL, temperature=0.0, max_tokens=900)
    try:
        structured = critic.with_structured_output(SectionReview)
    except Exception:
        structured = None

    for section_id, markdown in state.get("sections", {}).items():
        audit = state.get("audits", {}).get(section_id, {"hard": [], "soft": [], "checked": 0})
        if not routed.get(section_id):
            reviews[section_id] = {"verdict": "pass", "problems": [], "instructions": ""}
            continue
        # A clean section needs no model call at all. One lone note is not
        # worth a full review round on a free-tier token budget.
        if not audit.get("hard") and len(audit.get("soft", [])) < 2:
            reviews[section_id] = {"verdict": "pass", "problems": [], "instructions": ""}
            continue

        allowed = "\n".join(f"- {c.url}" for c in routed.get(section_id, []))
        audit_text = "\n".join(f"- {p}" for p in (audit.get("hard", []) + audit.get("soft", []))) or "- none"
        user = prompts.CRITIC_USER.format(
            title=SECTION_BY_ID[section_id].title,
            audit=audit_text,
            allowed=allowed,
            draft=markdown,
        )
        messages = [SystemMessage(content=prompts.CRITIC_SYSTEM), HumanMessage(content=user)]

        review = {"verdict": "pass", "problems": [], "instructions": ""}
        try:
            if structured is not None:
                with _SEM:
                    result: SectionReview = structured.invoke(messages)
                review = result.model_dump()
            else:
                raw = _invoke(_llm(model=CRITIC_MODEL, temperature=0.0), messages)
                parsed = _extract_json(raw)
                review = {
                    "verdict": parsed.get("verdict", "pass"),
                    "problems": parsed.get("problems", []),
                    "instructions": parsed.get("instructions", ""),
                }
        except Exception:
            review = {"verdict": "pass", "problems": [], "instructions": ""}

        # A hard deterministic failure always forces a revision,
        # even if the LLM critic was lenient.
        if audit.get("hard"):
            review["verdict"] = "revise"
            review["problems"] = list(dict.fromkeys(audit["hard"] + list(review.get("problems", []))))
            review["instructions"] = review.get("instructions") or "Remove or replace unsupported links and fix structure."

        reviews[section_id] = review

    return {"reviews": reviews}


def _route_after_critic(state: BriefState) -> str:
    revisions = state.get("revisions", 0)
    if revisions >= MAX_REVISIONS:
        return "brief"
    flagged = [k for k, v in state.get("reviews", {}).items() if v.get("verdict") == "revise"]
    return "revise" if flagged else "brief"


def _node_revise(state: BriefState) -> dict:
    progress = state.get("progress") or (lambda *_: None)
    flagged = [k for k, v in state.get("reviews", {}).items() if v.get("verdict") == "revise"]
    progress(f"Revising {len(flagged)} section(s) flagged by the editor…", 0.88)

    routed = state.get("routed", {})
    sections = dict(state.get("sections", {}))
    revisions = state.get("revisions", 0) + 1
    lock = threading.Lock()
    done = 0
    total = max(len(flagged), 1)

    def work(section_id: str) -> tuple[str, str]:
        nonlocal done
        review = state.get("reviews", {}).get(section_id, {})
        pool = "\n".join(c.to_prompt() for c in routed.get(section_id, []))
        user = prompts.REVISE_USER.format(
            problems="\n".join(f"- {p}" for p in review.get("problems", [])) or "- accuracy",
            instructions=review.get("instructions", "Fix the problems listed."),
            pool=pool,
            draft=sections.get(section_id, ""),
        )
        try:
            text = _invoke(
                _llm(temperature=0.15),
                [SystemMessage(content=prompts.WRITER_SYSTEM), HumanMessage(content=user)],
            )
            result = _strip_fences(text)
        except Exception:  # noqa: BLE001
            # Keep the previous draft rather than losing the section.
            result = sections.get(section_id, "")
        with lock:
            done += 1
            progress(
                f"Revised {done}/{total} flagged section(s)",
                0.88 + 0.03 * (done / total),
            )
        return section_id, result

    with ThreadPoolExecutor(max_workers=max(1, LLM_CONCURRENCY)) as pool:
        for section_id, text in pool.map(work, flagged):
            sections[section_id] = text

    return {"sections": sections, "revisions": revisions}


def _sections_digest(state: BriefState, limit: int = 6000) -> str:
    parts = []
    for section in _active_sections(state):
        text = state.get("sections", {}).get(section.id, "")
        parts.append(f"### {section.title}\n{text}")
    digest = "\n\n".join(parts)
    return digest[:limit]


def _node_brief(state: BriefState) -> dict:
    progress = state.get("progress") or (lambda *_: None)
    progress("Writing the executive summary and closing summary…", 0.91)

    user = prompts.BRIEF_USER.format(today=today_human(), sections=_sections_digest(state))
    try:
        brief = _invoke(
            _llm(temperature=0.3, max_tokens=2000),
            [SystemMessage(content=prompts.BRIEF_SYSTEM), HumanMessage(content=user)],
        )
    except Exception:  # noqa: BLE001
        brief = ""

    progress("Building the learning corner and vocabulary…", 0.94)
    learning_user = prompts.LEARNING_USER.format(today=today_human(), sections=_sections_digest(state, 5000))
    learning: dict[str, Any] = {}
    try:
        pack = _llm(temperature=0.2, max_tokens=2500).with_structured_output(LearningPack)
        with _SEM:
            result = pack.invoke(
                [SystemMessage(content=prompts.LEARNING_SYSTEM), HumanMessage(content=learning_user)]
            )
        learning = result.model_dump()
    except Exception:
        try:
            raw = _invoke(
                _llm(temperature=0.2, max_tokens=1400),
                [SystemMessage(content=prompts.LEARNING_SYSTEM), HumanMessage(content=learning_user)],
            )
            learning = _extract_json(raw)
        except Exception:
            learning = {}

    return {"brief": _strip_fences(brief), "learning": learning}


def _node_assemble(state: BriefState) -> dict:
    progress = state.get("progress") or (lambda *_: None)
    progress("Assembling the final report…", 0.97)

    active = _active_sections(state)
    section_titles = {s.id: s.title for s in active}
    sources = build_source_index(state.get("sections", {}), section_titles)
    # Count stories that actually made it into the text, not candidates routed.
    story_counts = {
        sid: len(re.findall(r"^###\s+", md, flags=re.M))
        for sid, md in state.get("sections", {}).items()
    }
    report = assemble_report(
        sections=state.get("sections", {}),
        brief=state.get("brief", ""),
        learning=state.get("learning", {}),
        sources=sources,
        audits=state.get("audits", {}),
        story_counts=story_counts,
        total_candidates=len(state.get("candidates", [])),
        window_days=state.get("days") or NEWS_WINDOW_DAYS,
        active_sections=[s.id for s in active],
    )
    return {"report": report}


# --------------------------------------------------------------------------
# Graph
# --------------------------------------------------------------------------
def build_graph():
    builder = StateGraph(BriefState)
    builder.add_node("prepare", _node_prepare)
    builder.add_node("write", _node_write)
    builder.add_node("audit", _node_audit)
    builder.add_node("critic", _node_critic)
    builder.add_node("revise", _node_revise)
    builder.add_node("brief", _node_brief)
    builder.add_node("assemble", _node_assemble)

    builder.add_edge(START, "prepare")
    builder.add_edge("prepare", "write")
    builder.add_edge("write", "audit")
    builder.add_edge("audit", "critic")
    builder.add_conditional_edges(
        "critic", _route_after_critic, {"revise": "revise", "brief": "brief"}
    )
    builder.add_edge("revise", "audit")
    builder.add_edge("brief", "assemble")
    builder.add_edge("assemble", END)
    return builder.compile()


def run_briefing(
    progress: Progress | None = None,
    days: int | None = None,
    max_stories: int | None = None,
    sections: list[str] | None = None,
) -> dict:
    """Run the full pipeline and return the final state."""
    _require_keys()

    # The UI passes section *titles*; the pipeline works with ids.
    title_to_id = {s.title: s.id for s in SECTIONS}
    if sections:
        section_ids = [title_to_id[t] for t in sections if t in title_to_id]
    else:
        section_ids = [s.id for s in SECTIONS]
    if not section_ids:
        section_ids = [s.id for s in SECTIONS]

    graph = build_graph()
    initial: BriefState = {
        "progress": progress or (lambda *_: None),
        "revisions": 0,
        "days": max(1, int(days or NEWS_WINDOW_DAYS)),
        "max_stories": max(1, int(max_stories or MAX_STORIES_PER_SECTION)),
        "section_ids": section_ids,
    }
    return graph.invoke(initial)
