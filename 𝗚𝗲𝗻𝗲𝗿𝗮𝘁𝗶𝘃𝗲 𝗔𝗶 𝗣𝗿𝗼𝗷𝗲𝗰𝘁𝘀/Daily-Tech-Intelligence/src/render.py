"""Assemble the final Markdown report."""
from __future__ import annotations

from datetime import datetime

from .config import APP_NAME, APP_OWNER, NEWS_WINDOW_DAYS, SECTIONS, VERSION

_NUMERALS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]


def _split_brief(brief: str) -> tuple[str, str]:
    """Move the '## Final Summary' block to the end of the report."""
    marker = "## Final Summary"
    idx = (brief or "").find(marker)
    if idx == -1:
        return brief or "", ""
    return brief[:idx].rstrip(), brief[idx:].strip()


def _verification_table(
    audits: dict[str, dict],
    story_counts: dict[str, int],
    sections: list | None = None,
) -> str:
    rows = [
        "| Section | Stories | Links checked | Automated checks |",
        "|---|---:|---:|---|",
    ]
    for section in (sections or SECTIONS):
        audit = audits.get(section.id, {})
        hard = len(audit.get("hard", []))
        soft = len(audit.get("soft", []))
        checked = audit.get("checked", 0)
        stories = story_counts.get(section.id, 0)
        if stories == 0:
            status = "no matching news"
        elif hard:
            status = f"⚠️ {hard} unresolved issue(s)"
        elif soft:
            status = f"✅ passed · {soft} note(s)"
        else:
            status = "✅ passed"
        rows.append(f"| {section.title} | {stories} | {checked} | {status} |")
    return "\n".join(rows)


def _vocabulary_table(terms: list[dict]) -> str:
    rows = [
        "| Technical Term | Simple Definition | Practical Example |",
        "|---|---|---|",
    ]
    for item in terms[:10]:
        if not isinstance(item, dict):
            continue
        term = str(item.get("term", "")).strip()
        definition = str(item.get("definition", "")).strip()
        example = str(item.get("example", "")).strip()
        if not term:
            continue
        rows.append(f"| **{term}** | {definition} | {example} |")
    return "\n".join(rows) if len(rows) > 2 else "_No vocabulary generated for this run._"


def assemble_report(
    sections: dict[str, str],
    brief: str,
    learning: dict,
    sources: str,
    audits: dict[str, dict],
    story_counts: dict[str, int],
    total_candidates: int,
    window_days: int = NEWS_WINDOW_DAYS,
    active_sections: list[str] | None = None,
) -> str:
    now = datetime.now()
    date_human = now.strftime("%A, %d %B %Y")
    time_human = now.strftime("%H:%M")

    selected = [s for s in SECTIONS if not active_sections or s.id in active_sections]
    if not selected:
        selected = list(SECTIONS)

    head, final_summary = _split_brief(brief)

    total_stories = sum(story_counts.values())
    parts: list[str] = []

    # ---------------- Header ----------------
    parts.append(
        f"# {APP_NAME}\n\n"
        f"**Prepared for {APP_OWNER}**  \n"
        f"{date_human} · generated at {time_human}\n\n"
        f"> A verified daily briefing across artificial intelligence, software, "
        f"robotics and research — built from official announcements and credible "
        f"reporting from the last {window_days} days.\n\n"
        f"| | |\n|---|---|\n"
        f"| **Stories selected** | {total_stories} |\n"
        f"| **Unique stories screened** | {total_candidates} |\n"
        f"| **Sections covered** | {sum(1 for s in selected if story_counts.get(s.id, 0))} of {len(selected)} |\n"
        f"| **News window** | last {window_days} days |\n"
        f"| **Verification** | link + source + claim spot-checks, then editor review |\n"
    )

    # ---------------- Contents ----------------
    contents = "\n".join(
        f"- {_NUMERALS[i]}. {s.title}" for i, s in enumerate(selected)
    )
    parts.append(
        "---\n\n"
        "**In this briefing**\n\n"
        f"{contents}\n"
        "- AI Engineering Learning Corner\n"
        "- Technical Vocabulary\n"
        "- Sources & verification\n"
    )

    # ---------------- Executive layer ----------------
    if head:
        parts.append("---\n\n" + head)

    # ---------------- Sections ----------------
    for i, section in enumerate(selected):
        body = sections.get(section.id, "").strip() or "_No content generated._"
        parts.append(f"---\n\n## {_NUMERALS[i]}. {section.emoji} {section.title}\n\n{body}")

    # ---------------- Learning corner ----------------
    concept = str(learning.get("concept", "")).strip()
    explanation = str(learning.get("concept_explanation", "")).strip()
    experiment = str(learning.get("experiment", "")).strip()

    if concept or explanation or experiment:
        block = ["---\n\n## 🎓 AI Engineering Learning Corner\n"]
        if concept:
            block.append(f"### Concept of the day: {concept}\n")
        if explanation:
            block.append(explanation + "\n")
        if experiment:
            block.append(f"**Try this today**\n\n{experiment}\n")
        parts.append("\n".join(block))

    # ---------------- Vocabulary ----------------
    terms = learning.get("terms") or []
    if terms:
        parts.append(
            "---\n\n## 📚 Technical Vocabulary\n\n"
            "| Technical Term | Simple Definition | Practical Example |\n"
            "|---|---|---|\n"
            + "\n".join(_vocabulary_table(terms).splitlines()[2:])
        )

    # ---------------- Final summary ----------------
    final_block = ["---\n\n## 🧭 Final Summary\n"]
    if final_summary:
        # Drop the original heading, keep its content.
        content = final_summary.split("\n", 1)[1] if "\n" in final_summary else ""
        final_block.append(content.strip() + "\n")

    if concept:
        final_block.append(f"**5. One important AI Engineering concept to learn**\n\n{concept} — {explanation.split('.')[0]}.\n")

    recommendations = learning.get("recommendations") or []
    if recommendations:
        items = "\n".join(f"{i + 1}. {r}" for i, r in enumerate(recommendations[:3]))
        final_block.append(f"**6. Three practical learning recommendations**\n\n{items}\n")

    parts.append("\n".join(final_block))

    # ---------------- Sources ----------------
    parts.append("---\n\n## 🔗 Sources\n\n" + sources)

    # ---------------- Verification ----------------
    parts.append(
        "---\n\n## 🛡️ Verification Notes\n\n"
        "Every link in this report was checked against the set of articles actually "
        "fetched for this run. A link that was not in that set was rejected. "
        "Claim spot-checks compare the wording of the report against the text of "
        "the source page.\n\n"
        + _verification_table(audits, story_counts, selected)
        + "\n\n> **Limits of this check:** it confirms that a source exists, that the "
        "link is real and that the wording overlaps. It does not guarantee that a "
        "company's claim is true — treat vendor claims as claims, not facts.\n"
    )

    # ---------------- Footer ----------------
    parts.append(
        "---\n\n"
        f"*{APP_NAME} v{VERSION} · built by {APP_OWNER} · "
        f"pipeline: Tavily + arXiv + GitHub + Hacker News → LangGraph writers → "
        f"deterministic audit → editor agent → report*"
    )

    return "\n\n".join(part for part in parts if part.strip())
