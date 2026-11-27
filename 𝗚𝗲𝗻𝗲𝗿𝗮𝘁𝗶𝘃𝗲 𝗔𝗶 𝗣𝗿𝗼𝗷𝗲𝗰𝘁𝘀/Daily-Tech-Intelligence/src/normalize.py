"""
Normalisation: de-duplicate, cluster the same story across outlets,
score by recency + source quality, and route items to sections.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlunparse

from .config import MAX_CANDIDATES_PER_SECTION, NEWS_WINDOW_DAYS, OFFICIAL_DOMAINS, SECTION_KEYWORDS, SECTIONS
from .schemas import Candidate

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "at",
    "by", "from", "as", "is", "are", "was", "were", "be", "been", "its", "it",
    "this", "that", "these", "those", "new", "says", "said", "will", "can",
    "how", "why", "what", "who", "after", "before", "over", "into", "about",
    "more", "than", "you", "your", "we", "our", "they", "their", "has", "have",
}


def canonical_url(url: str) -> str:
    try:
        p = urlparse(url)
        host = (p.netloc or "").replace("www.", "").lower()
        path = (p.path or "/").rstrip("/")
        return urlunparse((p.scheme or "https", host, path, "", "", ""))
    except Exception:
        return url


def title_tokens(title: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", (title or "").lower())
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _recency_score(published: str, days: int | None = None) -> float:
    if not published:
        return 0.35
    try:
        d = datetime.strptime(published, "%Y-%m-%d")
    except ValueError:
        return 0.35
    age_days = max((datetime.now() - d).days, 0)
    return max(0.0, 1.0 - age_days / max(days or NEWS_WINDOW_DAYS, 1))


def _source_score(candidate: Candidate) -> float:
    if candidate.origin == "arxiv":
        return 0.9
    if candidate.origin == "github":
        return 0.8
    host = candidate.domain
    if any(host == d or host.endswith("." + d) for d in OFFICIAL_DOMAINS):
        return 1.0
    if candidate.origin == "hackernews":
        return 0.55
    return 0.7


def _keyword_score(candidate: Candidate) -> float:
    text = f"{candidate.title} {candidate.snippet}".lower()
    hits = 0
    for words in SECTION_KEYWORDS.values():
        hits += sum(1 for w in words if w in text)
    return min(hits / 12.0, 1.0)


def dedupe_and_cluster(
    candidates: list[Candidate],
    threshold: float = 0.52,
    days: int | None = None,
) -> list[Candidate]:
    """
    Collapse the same story reported by multiple outlets.

    We keep the highest-quality representative and record how many
    independent sources covered it (that is a real signal of importance).
    """
    seen_urls: set[str] = set()
    unique: list[Candidate] = []
    for c in candidates:
        cu = canonical_url(c.url)
        if not cu or cu in seen_urls or not c.title:
            continue
        seen_urls.add(cu)
        unique.append(c)

    token_map = [(c, title_tokens(c.title)) for c in unique]
    clusters: list[list[tuple[Candidate, set[str]]]] = []
    for item in token_map:
        placed = False
        for cluster in clusters:
            if jaccard(item[1], cluster[0][1]) >= threshold:
                cluster.append(item)
                placed = True
                break
        if not placed:
            clusters.append([item])

    result: list[Candidate] = []
    for cluster in clusters:
        best = max(
            (c for c, _ in cluster),
            key=lambda c: (_source_score(c), _recency_score(c.published, days), len(c.snippet)),
        )
        coverage = len({c.domain for c, _ in cluster})
        # Coverage bonus is real importance evidence, not decoration.
        best.score = (
            0.45 * _source_score(best)
            + 0.30 * _recency_score(best.published, days)
            + 0.15 * _keyword_score(best)
            + 0.10 * min(coverage / 3.0, 1.0)
        )
        result.append(best)

    result.sort(key=lambda c: c.score, reverse=True)
    return result


def _matches(section_id: str, candidate: Candidate) -> int:
    text = f"{candidate.title} {candidate.snippet}".lower()
    return sum(1 for kw in SECTION_KEYWORDS.get(section_id, ()) if kw in text)


def route_to_sections(candidates: list[Candidate]) -> dict[str, list[Candidate]]:
    """
    Assign each candidate to the section(s) it best fits.

    A candidate can serve more than one section, but each section only sees
    its top-N by score, which keeps prompts small and focused.
    """
    routed: dict[str, list[Candidate]] = {s.id: [] for s in SECTIONS}

    for c in candidates:
        scores = {s.id: _matches(s.id, c) for s in SECTIONS}

        # Hard routing for structured sources.
        if c.origin == "arxiv":
            scores["research"] += 5
            scores["ai"] += 2
        if c.origin == "github":
            scores["dev"] += 5
            scores["tools"] += 2

        ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        top_id, top_score = ranked[0]
        if top_score == 0:
            # No keyword signal: put general news in AI, the widest bucket.
            top_id = "ai"
        routed[top_id].append(c)

        # Allow a strong secondary match as well.
        if len(ranked) > 1 and ranked[1][1] > 0 and ranked[1][1] >= max(1, top_score - 1):
            routed[ranked[1][0]].append(c)

    for sid, items in routed.items():
        items.sort(key=lambda c: c.score, reverse=True)
        routed[sid] = items[:MAX_CANDIDATES_PER_SECTION]

    return routed


def prepare(
    candidates: list[Candidate],
    days: int | None = None,
) -> tuple[list[Candidate], dict[str, list[Candidate]]]:
    cleaned = dedupe_and_cluster(candidates, days=days)
    routed = route_to_sections(cleaned)
    return cleaned, routed


def section_is_empty(routed: dict[str, list[Candidate]], section_id: str) -> bool:
    return not routed.get(section_id)
