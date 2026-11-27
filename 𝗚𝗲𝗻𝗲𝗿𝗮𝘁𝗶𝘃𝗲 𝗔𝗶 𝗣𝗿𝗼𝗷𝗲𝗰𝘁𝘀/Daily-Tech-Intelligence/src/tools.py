"""
Verification tools.

This module is what stops the report from becoming a confident liar.

Two layers:

1. Deterministic checks (strong, cheap, reliable)
   - every URL in the report must exist in the fetched candidate pool
   - every story must carry at least one source link
   - spot-check: does the source page actually contain the claim?

2. The LLM critic (see graph.py) receives these findings and reviews
   structure, labelling and completeness on top.

A plain LLM "critic" alone cannot verify facts, because it shares the
writer's blind spots. Fetching the page can.
"""
from __future__ import annotations

import re
import threading
from functools import lru_cache

import requests

from .config import FETCH_TIMEOUT, MAX_FETCH_CHECKS

_PAGE_CACHE: dict[str, str] = {}
_CACHE_LOCK = threading.Lock()

_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "at",
    "by", "from", "as", "is", "are", "was", "were", "be", "been", "its", "it",
    "this", "that", "these", "those", "new", "says", "said", "will", "can",
    "has", "have", "had", "but", "not", "you", "your", "we", "our", "they",
}


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z0-9]+", (text or "").lower())
    return {w for w in words if len(w) > 3 and w not in _STOP}


def fetch_page(url: str) -> str:
    """Fetch and extract readable text from a URL. Cached per process."""
    with _CACHE_LOCK:
        if url in _PAGE_CACHE:
            return _PAGE_CACHE[url]

    text = ""
    try:
        import trafilatura

        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded) or ""
    except Exception:
        text = ""

    if not text:
        try:
            r = requests.get(
                url,
                timeout=FETCH_TIMEOUT,
                headers={"User-Agent": "Mozilla/5.0 (compatible; TechBriefing/1.0)"},
            )
            if r.ok:
                from bs4 import BeautifulSoup

                soup = BeautifulSoup(r.text, "html.parser")
                for tag in soup(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()
                text = soup.get_text(" ", strip=True)
        except Exception:
            text = ""

    text = re.sub(r"\s+", " ", text or "").strip()
    with _CACHE_LOCK:
        _PAGE_CACHE[url] = text
    return text


def extract_links(markdown: str) -> list[str]:
    links = re.findall(r"\]\((https?://[^)\s]+)\)", markdown or "")
    cleaned = []
    for link in links:
        link = link.strip().rstrip(".,;:!?)")
        if link and link not in cleaned:
            cleaned.append(link)
    return cleaned


def _sentence_around(markdown: str, url: str) -> str:
    idx = markdown.find(url)
    if idx == -1:
        return ""
    start = max(0, idx - 400)
    window = markdown[start: idx + len(url) + 200]
    parts = re.split(r"(?<=[.!?])\s+", window)
    best = ""
    for part in parts:
        if url in part:
            best = part
            break
    return best.replace(url, " ")


def _normalise_url(url: str) -> str:
    return url.split("#")[0].rstrip("/").lower()


# Numbers are where models fabricate most confidently, and they are the
# easiest thing to verify mechanically. "3-5% MAE" and "30 fps" are checkable;
# prose is not.
_NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*")
_LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)\s]+)\)")

# A sentence carrying any of these is making a quantitative claim.
_QUANTITATIVE = re.compile(
    r"%|\bfps\b|\$|€|£|\bbillion\b|\bmillion\b|\btrillion\b|\bGB\b|\bTB\b"
    r"|\btokens?\b|\bparams?\b|\bms\b|\bx\s+(?:faster|slower|more|less)\b",
    re.IGNORECASE,
)


def _numbers(text: str) -> set[str]:
    """Extract comparable numeric tokens, ignoring years and URLs."""
    text = _LINK_RE.sub(lambda m: m.group(1), text or "")
    text = re.sub(r"https?://\S+", " ", text)
    # Drop metadata lines whose numbers are dates, not claims.
    text = re.sub(r"^\*\*Date:\*\*.*$", " ", text, flags=re.M)
    found: set[str] = set()
    for raw in _NUMBER_RE.findall(text):
        token = raw.replace(",", "").rstrip(".")
        if not token:
            continue
        # Years are usually formatting, not claims.
        if re.fullmatch(r"(19|20)\d{2}", token):
            continue
        # Drop trailing zeros so "30.0" and "30" compare equal.
        if "." in token:
            token = token.rstrip("0").rstrip(".")
        found.add(token)
    return found


def audit_numbers(markdown: str, source_text: str) -> dict:
    """
    Flag numbers in the draft that appear nowhere in the source material.

    A figure that is in neither the fetched snippet nor the cited page was
    almost certainly invented. Quantitative sentences (percentages, speeds,
    prices, model sizes) are hard failures; stray small integers are notes.
    """
    available = _numbers(source_text)
    hard: list[str] = []
    soft: list[str] = []

    for sentence in re.split(r"(?<=[.!?])\s+|\n", markdown or ""):
        claimed = _numbers(sentence)
        if not claimed:
            continue
        missing = claimed - available
        if not missing:
            continue
        quantitative = bool(_QUANTITATIVE.search(sentence))
        # Long numbers are almost always specs or statistics, not prose.
        large = {t for t in missing if len(t.split(".")[0]) >= 3}
        if quantitative or large:
            hard.extend(sorted(missing, key=lambda x: (-len(x), x)))
        else:
            soft.extend(sorted(missing, key=lambda x: (-len(x), x)))

    def _msg(items: list[str], label: str) -> list[str]:
        uniq = list(dict.fromkeys(items))
        if not uniq:
            return []
        return [
            f"{label} not found in any cited source: "
            + ", ".join(uniq[:8])
            + ". Use the exact figures the sources state, or remove them."
        ]

    return {
        "hard": _msg(hard, "Unverified number(s)"),
        "soft": _msg(soft, "Unconfirmed number(s)"),
    }


def audit_section(
    markdown: str,
    allowed_urls: set[str],
    source_text: str = "",
) -> dict:
    """
    Run deterministic checks on one generated section.

    Returns {"hard": [...], "soft": [...], "checked": int}
    `hard` issues force a rewrite. `soft` issues are context for the critic.
    """
    hard: list[str] = []
    soft: list[str] = []

    if not markdown or len(markdown.strip()) < 120:
        hard.append("Section is empty or far too short.")
        return {"hard": hard, "soft": soft, "checked": 0}

    links = extract_links(markdown)
    allowed = {_normalise_url(u) for u in allowed_urls}

    unknown = [u for u in links if _normalise_url(u) not in allowed]
    for u in unknown[:6]:
        hard.append(
            f"Link not present in the verified source pool: {u} "
            "(this is either invented or copied incorrectly — remove or replace it)."
        )

    story_count = len(re.findall(r"^###\s+", markdown, flags=re.M))
    source_blocks = len(re.findall(r"\*\*Sources?:\*\*", markdown, flags=re.I))
    if story_count == 0:
        hard.append("No story sub-headings found (expected markdown '### Headline').")
    elif source_blocks < story_count:
        soft.append(
            f"{story_count} stories but only {source_blocks} '**Sources:**' blocks. "
            "Every story needs at least one source link."
        )

    # Spot-check a handful of pages: does the page actually support the claim?
    checked = 0
    page_corpus: list[str] = []
    for url in links:
        if checked >= MAX_FETCH_CHECKS:
            break
        if _normalise_url(url) not in allowed:
            continue
        page = fetch_page(url)
        checked += 1
        if not page:
            soft.append(f"Could not fetch {url} to verify (page may block bots).")
            continue
        page_corpus.append(page[:20000])
        claim = _sentence_around(markdown, url)
        claim_tokens = _tokens(claim)
        if len(claim_tokens) < 4:
            continue
        page_tokens = _tokens(page[:20000])
        overlap = len(claim_tokens & page_tokens) / len(claim_tokens)
        if overlap < 0.20:
            soft.append(
                f"Weak textual overlap ({overlap:.0%}) between the claim and {url}. "
                "Re-check that the claim is actually supported by that source."
            )

    # Numbers must come from the material the writer was given, or from the
    # page itself. Anything else is invented — but only trust a hard failure
    # when we actually managed to read a page; otherwise the source snippet is
    # all we have and it is truncated.
    corpus = " ".join([source_text] + page_corpus)
    if corpus.strip():
        number_findings = audit_numbers(markdown, corpus)
        if page_corpus:
            hard.extend(number_findings["hard"])
            soft.extend(number_findings["soft"])
        else:
            soft.extend(number_findings["hard"] + number_findings["soft"])

    return {"hard": hard, "soft": soft, "checked": checked}


def build_source_index(section_markdown: dict[str, str], section_titles: dict[str, str]) -> str:
    """A deduplicated source appendix grouped by section."""
    lines: list[str] = []
    seen: set[str] = set()
    for sid, md in section_markdown.items():
        links = extract_links(md)
        if not links:
            continue
        lines.append(f"\n**{section_titles.get(sid, sid)}**\n")
        for url in links:
            key = _normalise_url(url)
            if key in seen:
                continue
            seen.add(key)
            host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
            lines.append(f"- [{host}]({url})")
    return "\n".join(lines) if lines else "_No sources recorded._"
