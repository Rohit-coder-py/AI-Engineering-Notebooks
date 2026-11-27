"""
Central configuration for the Daily Technology Intelligence briefing.

Everything tunable lives here so the rest of the code stays clean.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

APP_NAME = "Daily Technology Intelligence"
APP_OWNER = "Rohit Jha"
APP_TAGLINE = "A verified, daily briefing across AI, software, robotics and research."
VERSION = "1.0.0"

# --------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
CRITIC_MODEL = os.getenv("CRITIC_MODEL", GROQ_MODEL)
# gpt-oss / qwen3 models on Groq spend part of the token budget on reasoning.
# "low" keeps latency and cost down without hurting factual writing.
REASONING_EFFORT = os.getenv("REASONING_EFFORT", "low")

# --------------------------------------------------------------------------
# Pipeline limits
# --------------------------------------------------------------------------
NEWS_WINDOW_DAYS = int(os.getenv("NEWS_WINDOW_DAYS", "2"))
MAX_STORIES_PER_SECTION = int(os.getenv("MAX_STORIES_PER_SECTION", "5"))
MAX_CANDIDATES_PER_SECTION = int(os.getenv("MAX_CANDIDATES_PER_SECTION", "7"))
MAX_REVISIONS = int(os.getenv("MAX_REVISIONS", "1"))
LLM_CONCURRENCY = int(os.getenv("LLM_CONCURRENCY", "2"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4000"))
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))
FETCH_TIMEOUT = int(os.getenv("FETCH_TIMEOUT", "12"))
MAX_FETCH_CHECKS = int(os.getenv("MAX_FETCH_CHECKS", "4"))

# --------------------------------------------------------------------------
# Source quality tiers
# --------------------------------------------------------------------------
# Tier 1: primary / official sources. Strongly preferred.
OFFICIAL_DOMAINS = [
    "openai.com", "blog.google", "deepmind.google", "research.google",
    "anthropic.com", "nvidia.com", "blogs.nvidia.com", "microsoft.com",
    "azure.microsoft.com", "meta.com", "ai.meta.com", "x.ai", "apple.com",
    "aws.amazon.com", "cloud.google.com", "huggingface.co", "arxiv.org",
    "github.blog", "blog.cloudflare.com", "mistral.ai", "cohere.com",
    "stability.ai", "runwayml.com", "perplexity.ai", "elevenlabs.io",
    "groq.com", "together.ai", "fireworks.ai", "modal.com", "replicate.com",
    "langchain.com", "llamaindex.ai", "ollama.com", "vercel.com",
    "ibm.com", "research.ibm.com", "samsung.com", "qualcomm.com", "arm.com",
    "intel.com", "amd.com", "boston-dynamics.com", "figure.ai", "waymo.com",
    "openrouter.ai", "wandb.com", "databricks.com",
]

# Tier 2: credible independent reporting.
TRUSTED_DOMAINS = [
    "techcrunch.com", "theverge.com", "venturebeat.com", "reuters.com",
    "wired.com", "arstechnica.com", "bloomberg.com", "ft.com",
    "technologyreview.com", "theinformation.com", "semianalysis.com",
    "zdnet.com", "thenextweb.com", "axios.com", "cnbc.com",
    "newscientist.com", "nature.com", "science.org", "spectrum.ieee.org",
    "tomshardware.com", "anandtech.com", "engadget.com",
    "theguardian.com", "bbc.com", "apnews.com", "businessinsider.com",
    "theregister.com", "techradar.com", "digitaltrends.com",
    "the-decoder.com", "marktechpost.com", "infoq.com",
    "semiengineering.com", "space.com", "spacenews.com",
    "phys.org", "scientificamerican.com", "quantamagazine.org",
    "cacm.acm.org", "openreview.net",
]

ALLOWED_DOMAINS = OFFICIAL_DOMAINS + TRUSTED_DOMAINS

# Domains we never want as a primary citation.
BLOCKED_DOMAINS = [
    "pinterest.com", "facebook.com", "instagram.com", "tiktok.com",
    "quora.com", "reddit.com", "medium.com", "substack.com",
]


# --------------------------------------------------------------------------
# Sections
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class Section:
    id: str
    title: str
    label: str          # short category label used in the report
    emoji: str
    queries: tuple[str, ...]
    focus: str          # instruction handed to the writer


SECTIONS: tuple[Section, ...] = (
    Section(
        id="ai",
        title="Artificial Intelligence",
        label="AI",
        emoji="🧠",
        queries=(
            "new AI model release announcement this week",
            "AI breakthrough research announcement",
            "multimodal AI model launch",
            "AI agents framework launch",
        ),
        focus=(
            "Frontier model releases, capability jumps, multimodal systems, "
            "AI agent platforms, and major AI industry announcements."
        ),
    ),
    Section(
        id="tools",
        title="New AI Tools & Models",
        label="TOOLS",
        emoji="🛠️",
        queries=(
            "new AI tool launched this week pricing",
            "new AI app release free tier",
            "AI coding assistant launch",
            "open source AI model release",
        ),
        focus=(
            "Tools and models a developer can actually sign up for or download "
            "today. Always state pricing and availability when the source says so."
        ),
    ),
    Section(
        id="industry",
        title="Technology Industry",
        label="INDUSTRY",
        emoji="🏢",
        queries=(
            "OpenAI announcement",
            "Google DeepMind announcement",
            "Anthropic announcement",
            "NVIDIA announcement",
            "Microsoft AI announcement",
            "Meta AI announcement",
        ),
        focus=(
            "Strategic moves from OpenAI, Google, Microsoft, Anthropic, xAI, "
            "NVIDIA, Meta, Apple, Amazon and other major technology companies."
        ),
    ),
    Section(
        id="dev",
        title="Software & Development",
        label="SOFTWARE",
        emoji="💻",
        queries=(
            "new Python library release",
            "open source AI framework release",
            "developer tool launch 2026",
            "GitHub trending AI repository",
        ),
        focus=(
            "Programming tools, Python libraries, frameworks, developer "
            "platforms, GitHub projects and open-source releases."
        ),
    ),
    Section(
        id="robotics",
        title="Robotics & Automation",
        label="ROBOTICS",
        emoji="🤖",
        queries=(
            "humanoid robot news",
            "autonomous systems announcement",
            "industrial automation robotics news",
        ),
        focus=(
            "Humanoid robots, autonomous vehicles and drones, industrial "
            "automation, and embodied AI."
        ),
    ),
    Section(
        id="other",
        title="Other Technology",
        label="INFRA",
        emoji="⚙️",
        queries=(
            "cybersecurity AI news",
            "semiconductor GPU announcement",
            "quantum computing breakthrough",
            "cloud computing announcement",
            "space technology news",
        ),
        focus=(
            "Cybersecurity, semiconductors and GPUs, cloud infrastructure, "
            "hardware, space technology and quantum computing."
        ),
    ),
    Section(
        id="research",
        title="AI Research",
        label="RESEARCH",
        emoji="🔬",
        queries=(
            "AI research paper breakthrough",
            "machine learning paper arxiv",
        ),
        focus=(
            "Important research papers and scientific breakthroughs. Explain the "
            "problem, the approach, the finding and why it matters."
        ),
    ),
)

SECTION_BY_ID = {s.id: s for s in SECTIONS}

# Keyword hints used to pre-assign candidates to sections (cheap routing).
SECTION_KEYWORDS: dict[str, tuple[str, ...]] = {
    "ai": (
        "model", "llm", "multimodal", "agent", "reasoning", "benchmark",
        "inference", "transformer", "diffusion", "openai", "anthropic",
        "gemini", "claude", "gpt", "llama", "mistral", "fine-tune",
    ),
    "tools": (
        "launch", "launched", "release", "released", "available", "pricing",
        "free tier", "beta", "tool", "app", "assistant", "copilot", "api",
        "waitlist", "open source",
    ),
    "industry": (
        "acquisition", "partnership", "investment", "funding", "valuation",
        "ceo", "layoff", "revenue", "deal", "lawsuit", "regulation",
        "openai", "google", "microsoft", "anthropic", "nvidia", "meta",
        "apple", "amazon", "xai",
    ),
    "dev": (
        "python", "library", "framework", "sdk", "github", "open source",
        "developer", "package", "cli", "compiler", "runtime", "release",
    ),
    "robotics": (
        "robot", "humanoid", "autonomous", "drone", "self-driving",
        "automation", "manipulation", "embodied", "warehouse",
    ),
    "other": (
        "security", "cyber", "vulnerability", "gpu", "chip", "semiconductor",
        "quantum", "cloud", "datacenter", "data center", "satellite",
        "space", "hardware", "arm", "tsmc",
    ),
    "research": (
        "paper", "arxiv", "study", "researchers", "benchmark", "dataset",
        "novel", "propose", "we present", "experiment",
    ),
}
