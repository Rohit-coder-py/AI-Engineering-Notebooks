"""
Ingestion layer.

Four free/cheap sources, all normalised into `Candidate` objects:

  * Tavily news search  -> primary source (official + credible outlets)
  * arXiv API           -> AI research section
  * GitHub search API   -> open-source / developer section
  * Hacker News API     -> early signal on developer tools

Every fetch is defensive: a failing source never kills the run.
"""
from __future__ import annotations

import os
import re
import threading
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from typing import Callable

import requests

from .config import (
    ALLOWED_DOMAINS,
    BLOCKED_DOMAINS,
    FETCH_TIMEOUT,
    NEWS_WINDOW_DAYS,
    SECTIONS,
)
from .schemas import Candidate

Progress = Callable[[str, float], None]


def _noop(_msg: str, _pct: float) -> None:
    pass


def _clean(text: str, limit: int = 600) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def _iso(value: str | None) -> str:
    """Best-effort normalisation of assorted date strings to YYYY-MM-DD."""
    if not value:
        return ""
    value = str(value).strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", value)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    for fmt in ("%a, %d %b %Y %H:%M:%S %Z", "%Y-%m-%dT%H:%M:%SZ", "%d %b %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return ""


def _host(url: str) -> str:
    m = re.match(r"https?://([^/]+)", url or "")
    return m.group(1).replace("www.", "").lower() if m else ""


# --------------------------------------------------------------------------
# Tavily
# --------------------------------------------------------------------------
def tavily_news(
    queries: list[str],
    days: int | None = None,
    max_results: int = 8,
    progress: Progress = _noop,
) -> list[Candidate]:
    days = max(1, int(days or NEWS_WINDOW_DAYS))
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    if not api_key:
        return []

    try:
        from tavily import TavilyClient
    except ImportError:
        return []

    client = TavilyClient(api_key=api_key)
    out: list[Candidate] = []
    total = max(len(queries), 1)
    done = 0
    lock = threading.Lock()

    def search_one(query: str) -> list[Candidate]:
        nonlocal done
        found: list[Candidate] = []
        try:
            resp = client.search(
                query=query,
                topic="news",
                days=max(1, days),
                search_depth="advanced",
                include_domains=ALLOWED_DOMAINS,
                max_results=max_results,
            )
        except Exception:
            # Retry once without the domain filter (Tavily can reject huge lists).
            try:
                resp = client.search(
                    query=query,
                    topic="news",
                    days=max(1, days),
                    search_depth="basic",
                    max_results=max_results,
                )
            except Exception:
                with lock:
                    done += 1
                return found

        for item in resp.get("results", []):
            url = (item.get("url") or "").strip()
            host = _host(url)
            if not url or any(b in host for b in BLOCKED_DOMAINS):
                continue
            found.append(
                Candidate(
                    title=_clean(item.get("title", ""), 220),
                    url=url,
                    source=host or "unknown",
                    published=_iso(item.get("published_date")),
                    snippet=_clean(item.get("content", "")),
                    origin="tavily",
                )
            )

        with lock:
            done += 1
            progress(
                f"Searched {done}/{total} queries — {query[:48]}",
                0.05 + 0.35 * (done / total),
            )
        return found

    # Independent queries: running them in parallel is the difference between
    # a 2-minute and a 30-second ingestion step.
    with ThreadPoolExecutor(max_workers=4) as pool:
        for batch in pool.map(search_one, queries):
            out.extend(batch)

    return out


# --------------------------------------------------------------------------
# arXiv
# --------------------------------------------------------------------------
ARXIV_URL = "http://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"


def arxiv_latest(max_results: int = 12, progress: Progress = _noop) -> list[Candidate]:
    progress("Fetching arXiv (cs.AI, cs.LG, cs.CL)…", 0.42)
    query = "cat:cs.AI OR cat:cs.LG OR cat:cs.CL OR cat:cs.CV"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    try:
        r = requests.get(ARXIV_URL, params=params, timeout=FETCH_TIMEOUT)
        r.raise_for_status()
        root = ET.fromstring(r.text)
    except Exception:
        return []

    out: list[Candidate] = []
    for entry in root.findall(f"{ATOM}entry"):
        title = _clean((entry.findtext(f"{ATOM}title") or ""), 240)
        link = ""
        for ln in entry.findall(f"{ATOM}link"):
            if ln.get("rel") == "alternate":
                link = ln.get("href", "")
                break
        if not link:
            continue
        summary = _clean(entry.findtext(f"{ATOM}summary") or "", 700)
        published = _iso(entry.findtext(f"{ATOM}published") or "")
        authors = [a.findtext(f"{ATOM}name") or "" for a in entry.findall(f"{ATOM}author")][:3]
        author_str = ", ".join(a for a in authors if a)
        out.append(
            Candidate(
                title=title,
                url=link,
                source="arxiv.org",
                published=published,
                snippet=(f"{author_str}. {summary}" if author_str else summary),
                origin="arxiv",
            )
        )
    return out


# --------------------------------------------------------------------------
# GitHub
# --------------------------------------------------------------------------
def github_new_repos(max_results: int = 12, progress: Progress = _noop) -> list[Candidate]:
    progress("Fetching GitHub trending repositories…", 0.48)
    since = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        r = requests.get(
            "https://api.github.com/search/repositories",
            params={
                "q": f"created:>{since} stars:>25",
                "sort": "stars",
                "order": "desc",
                "per_page": max_results,
            },
            headers=headers,
            timeout=FETCH_TIMEOUT,
        )
        r.raise_for_status()
        items = r.json().get("items", [])
    except Exception:
        return []

    out: list[Candidate] = []
    for repo in items:
        desc = _clean(repo.get("description") or "", 400)
        topics = ", ".join(repo.get("topics") or [])
        out.append(
            Candidate(
                title=f"{repo.get('full_name', '')} — {desc[:120]}",
                url=repo.get("html_url", ""),
                source="github.com",
                published=_iso((repo.get("created_at") or "")[:10]),
                snippet=(
                    f"{desc} Language: {repo.get('language') or 'n/a'}. "
                    f"Stars: {repo.get('stargazers_count', 0)}. "
                    f"{('Topics: ' + topics) if topics else ''}"
                ),
                origin="github",
            )
        )
    return out


# --------------------------------------------------------------------------
# Hacker News (early developer signal)
# --------------------------------------------------------------------------
def hackernews(
    max_results: int = 10,
    days: int | None = None,
    progress: Progress = _noop,
) -> list[Candidate]:
    progress("Fetching Hacker News signal…", 0.52)
    window = max(1, int(days or NEWS_WINDOW_DAYS))
    since = int((datetime.now(timezone.utc) - timedelta(days=window)).timestamp())
    try:
        r = requests.get(
            "https://hn.algolia.com/api/v1/search",
            params={
                "tags": "story",
                "numericFilters": f"created_at_i>{since},points>60",
                "hitsPerPage": max_results,
            },
            timeout=FETCH_TIMEOUT,
        )
        r.raise_for_status()
        hits = r.json().get("hits", [])
    except Exception:
        return []

    out: list[Candidate] = []
    for h in hits:
        url = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
        title = _clean(h.get("title") or "", 220)
        if not title:
            continue
        out.append(
            Candidate(
                title=title,
                url=url,
                source=_host(url) or "news.ycombinator.com",
                published=_iso((h.get("created_at") or "")[:10]),
                snippet=(
                    f"{h.get('points', 0)} points, {h.get('num_comments', 0)} comments on Hacker News. "
                    f"{_clean(h.get('story_text') or '', 200)}"
                ),
                origin="hackernews",
            )
        )
    return out


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------
def gather(
    progress: Progress = _noop,
    days: int | None = None,
    section_ids: list[str] | None = None,
) -> list[Candidate]:
    """Fetch everything, returning one flat list of candidates."""
    window = max(1, int(days or NEWS_WINDOW_DAYS))
    active = {s.id for s in SECTIONS if not section_ids or s.id in section_ids}
    all_queries: list[str] = []
    for section in SECTIONS:
        if section.id not in active:
            continue
        for q in section.queries:
            if q not in all_queries:
                all_queries.append(q)

    progress("Starting ingestion…", 0.02)
    candidates: list[Candidate] = []
    candidates += tavily_news(all_queries, days=window, progress=progress)
    if "research" in active:
        candidates += arxiv_latest(progress=progress)
    if "dev" in active or "tools" in active:
        candidates += github_new_repos(progress=progress)
    candidates += hackernews(days=window, progress=progress)

    progress(f"Ingested {len(candidates)} raw items.", 0.55)
    return candidates
