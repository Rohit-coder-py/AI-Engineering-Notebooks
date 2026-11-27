"""Data models shared across the pipeline."""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------
# A single fetched news item
# --------------------------------------------------------------------------
@dataclass
class Candidate:
    title: str
    url: str
    source: str
    published: str                 # ISO date string, may be "" if unknown
    snippet: str
    origin: str                    # tavily | arxiv | github | hackernews
    score: float = 0.0
    sections: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return hashlib.sha1(self.url.encode("utf-8", "ignore")).hexdigest()[:10]

    @property
    def domain(self) -> str:
        m = re.match(r"https?://([^/]+)", self.url)
        return m.group(1).replace("www.", "").lower() if m else ""

    def to_prompt(self, max_snippet: int = 320) -> str:
        """Compact representation handed to the LLM."""
        snippet = re.sub(r"\s+", " ", self.snippet or "").strip()
        if len(snippet) > max_snippet:
            snippet = snippet[:max_snippet].rstrip() + "…"
        date = self.published or "date not stated by source"
        return (
            f"- id: {self.id}\n"
            f"  title: {self.title}\n"
            f"  url: {self.url}\n"
            f"  source: {self.source}\n"
            f"  published: {date}\n"
            f"  summary: {snippet}"
        )


# --------------------------------------------------------------------------
# LLM review models
# --------------------------------------------------------------------------
class SectionReview(BaseModel):
    """What the critic returns for one generated section."""

    verdict: Literal["pass", "revise"] = Field(
        description="pass if the section is publishable as-is, revise if not."
    )
    problems: list[str] = Field(
        default_factory=list,
        description="Concrete problems found. Empty when verdict is pass.",
    )
    instructions: str = Field(
        default="",
        description="Short, specific rewrite instructions for the writer.",
    )


class ToolPick(BaseModel):
    name: str
    what_it_does: str
    why_different: str
    try_this: str


class LearningPack(BaseModel):
    """Vocabulary + learning corner, generated in one call."""

    terms: list[dict[str, str]] = Field(
        default_factory=list,
        description="5-10 items with keys: term, definition, example",
    )
    concept: str = ""
    concept_explanation: str = ""
    experiment: str = ""
    recommendations: list[str] = Field(default_factory=list)


def today_human() -> str:
    return datetime.now().strftime("%A, %d %B %Y")


def today_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d")
