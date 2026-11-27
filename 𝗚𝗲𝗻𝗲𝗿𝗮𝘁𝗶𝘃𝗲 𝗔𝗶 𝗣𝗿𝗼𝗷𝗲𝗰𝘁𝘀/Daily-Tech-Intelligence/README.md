# 🛰️ Daily Technology Intelligence

**A verified, on-demand daily tech & AI briefing — built by Rohit Jha as a capstone project.**

Open the app, press one button, and get a complete Markdown briefing covering
seven areas of technology. Every link is checked against the articles that were
actually fetched, every statistic is checked against the source text, and a
separate editor agent reviews the writing before it reaches you.

No scheduler. No database. Nothing is stored between days — you generate a fresh
briefing whenever you want one.

---

## Why this exists

Reading tech news well is a skill: you need primary sources, you need to know
what is actually new, and you need to know what a claim is worth. Doing that
across AI, tooling, industry, software, robotics, infrastructure and research
takes an hour a day.

This app does the mechanical part — gathering, de-duplicating, ranking,
cross-checking — and leaves you the thinking. It also ends every briefing with a
learning corner, a vocabulary table and one experiment you can build the same
day, because the point is to get better at AI engineering, not just to read news.

---

## What you get

| Part | Contents |
|---|---|
| Header | Date, run stats, verification method |
| Executive Summary | The day's dominant theme in one paragraph |
| Story of the Day | The single most significant development |
| 1–7 | AI · New AI Tools & Models · Technology Industry · Software & Development · Robotics & Automation · Other Technology · AI Research |
| Per story | What happened / What's new / Important details / Why it matters / AI Engineering perspective / Sources |
| 🎓 Learning Corner | One concept explained properly + a sub-2-hour experiment |
| 📚 Technical Vocabulary | Term → plain-English definition → concrete example |
| 🧭 Final Summary | Six numbered takeaways |
| 🔗 Sources | Deduplicated source appendix grouped by section |
| 🛡️ Verification Notes | What was checked, and what the check does *not* prove |

Each story also carries an honest status label: **CONFIRMED**, **ANNOUNCED**,
**REPORTED** or **RUMOUR**.

---

## Quick start

```bash
cd "C:\Users\rohit\OneDrive\Desktop\Rohit-Jha-Daily-Tech-Intelligence"
pip install -r requirements.txt
copy .env.example .env      # then paste your two keys
streamlit run app.py
```

`.env` needs:

```
GROQ_API_KEY=gsk_...
TAVILY_API_KEY=tvly-...
```

Get them free at [console.groq.com](https://console.groq.com) and
[app.tavily.com](https://app.tavily.com). A `GITHUB_TOKEN` is optional and only
raises the GitHub search rate limit.

First run takes roughly 1–3 minutes depending on how many sections you keep
switched on.

---

## How it works

```
                 ┌──────────────┐
                 │   Streamlit  │  one button, sidebar controls
                 └──────┬───────┘
                        │
        ┌───────────────▼────────────────┐
        │  INGEST                        │
        │  Tavily news (per section)     │
        │  arXiv API    (research)       │
        │  GitHub API   (dev / tools)    │
        │  Hacker News  (early signal)   │
        └───────────────┬────────────────┘
                        │  raw candidates
        ┌───────────────▼────────────────┐
        │  NORMALISE                     │
        │  canonical URLs → dedupe       │
        │  Jaccard clustering of titles  │
        │  score = source + recency +    │
        │          keywords + coverage   │
        │  route to sections             │
        └───────────────┬────────────────┘
                        │  routed pools
        ┌───────────────▼────────────────┐
        │  WRITE  (parallel, 7 writers)  │  LangGraph fan-out
        └───────────────┬────────────────┘
                        │
        ┌───────────────▼────────────────┐
        │  AUDIT  (deterministic)        │
        │  • link must exist in pool     │
        │  • every story needs sources   │
        │  • claim ↔ page text overlap   │
        │  • numbers must appear in src  │
        └───────────────┬────────────────┘
                        │
        ┌───────────────▼────────────────┐
        │  EDITOR AGENT (LLM critic)     │
        │  accuracy, labelling, structure│
        └───────┬───────────────┬────────┘
                │ revise        │ pass
                ▼               │
        ┌───────────────┐       │   max 1 revision
        │   REVISE      │───────┘
        └───────────────┘
                        │
        ┌───────────────▼────────────────┐
        │  BRIEF + LEARNING PACK         │
        │  executive summary, story of   │
        │  the day, final summary,       │
        │  vocabulary, experiment        │
        └───────────────┬────────────────┘
                        │
        ┌───────────────▼────────────────┐
        │  ASSEMBLE → Markdown report    │
        └────────────────────────────────┘
```

### Why the verification layer matters

A "critic agent" that is just another LLM call shares the writer's blind spots:
if the writer invents a statistic, the critic will happily approve it, because
neither model has the source page in front of it.

So the app verifies **mechanically first**, then asks the model to review:

1. **Link integrity** — every URL in the draft must be present in the pool of
   articles actually fetched for this run. An invented or mistyped URL is a hard
   failure and forces a rewrite.
2. **Source presence** — every story must carry a `**Sources:**` block.
3. **Claim overlap** — the sentence making a claim is compared token-by-token
   against the live text of the cited page. Weak overlap is flagged.
4. **Numeric verification** — every number in a quantitative sentence (percentages,
   speeds, prices, model sizes) must appear in the source snippet or on the
   source page. Rounding, extrapolating or inventing a figure is a hard failure.

Only then does the editor agent review tone, rumour labelling and required
structure — and it receives the mechanical findings as evidence, so it can't
wave a broken link through.

> **Honest limit:** this proves a source exists, that the link is real, and that
> the wording and figures match it. It does **not** prove a company's claim is
> true. Vendor claims are reported as claims.

---

## The 90% reuse rule

The brief was to build this almost entirely from skills and libraries already
present in the `AI and Data Science` repository. That is how it is built — no new
framework, no new database, no new deployment stack.

| Capability | Where it already existed in the repo | How it is used here |
|---|---|---|
| Streamlit app structure, sidebar, `session_state`, custom CSS | `𝗦𝘁𝗿𝗲𝗮𝗺𝗹𝗶𝘁/` (`sidebar.py`, `st.session_state.py`, `designs_best.py`) | `app.py` — layout, hero, controls, tabs, downloads |
| LangChain prompt templates + system/user prompt design | `𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶/` (`chatprompttemplate.py`, `learning langchain.py`) | `src/prompts.py` |
| LangChain chat model wiring (Groq) | `𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶/` (`01_Integreting an AI model.py`) | `src/graph.py::_llm` |
| Structured output with Pydantic | `𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶/` (`core structred output.py`), `𝗣𝘆𝗱𝗮𝗻𝘁𝗶𝗰/` | `src/schemas.py` + critic and learning pack |
| arXiv paper fetching | `𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶/arvix.py` | `src/ingest.py::arxiv_latest` |
| Web/document loaders + text extraction | `𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶/` (`website data loader.py`, `docuement-loaders.py`) | `src/tools.py::fetch_page` |
| Multi-step agent workflow with critic + revision loop | `𝗔𝗜 𝗔𝗨𝗧𝗢𝗠𝗔𝗧𝗜𝗢𝗡 𝗪𝗼𝗿𝗸𝗳𝗹𝗼𝘄𝘀/`, `𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀/Aether` | `src/graph.py` (LangGraph state machine) |
| `.env` / API key handling | `𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀/Aether/.env` | `.env` + `python-dotenv` |
| Text cleaning, tokenisation, stopword handling | `𝗡𝗟𝗣(𝗡𝗮𝘁𝘂𝗿𝗮𝗹 𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴)/` | `src/normalize.py`, `src/tools.py` |
| Tables / tabular display | `𝗗𝗮𝘁𝗮 𝗔𝗻𝗮𝗹𝘆𝘀𝗶𝘀 𝗮𝗻𝗱 𝗩𝗶𝘀𝘂𝗮𝗹𝗶𝘇𝗮𝘁𝗶𝗼𝗻/` | verification table in the UI and the report |

Everything is a library already installed in that environment — Streamlit,
LangGraph, LangChain, langchain-groq, Tavily, Pydantic, trafilatura,
BeautifulSoup, pandas, requests, python-dotenv.

**The 10% that is genuinely new:** the verification design (`src/tools.py`), the
scoring and clustering logic (`src/normalize.py`), and the report layout
(`src/render.py`). No new dependency was introduced for any of it.

---

## Project layout

```
Rohit-Jha-Daily-Tech-Intelligence/
├── app.py                  Streamlit front-end
├── src/
│   ├── config.py           sections, queries, domain tiers, limits
│   ├── schemas.py          Pydantic models + Candidate dataclass
│   ├── ingest.py           Tavily · arXiv · GitHub · Hacker News
│   ├── normalize.py        dedupe, cluster, score, route
│   ├── tools.py            page fetch + deterministic verification
│   ├── prompts.py          every prompt in one place
│   ├── graph.py            LangGraph pipeline
│   └── render.py           Markdown assembly
├── .streamlit/config.toml  theme
├── requirements.txt
├── .env.example
└── README.md
```

---

## Controls

| Setting | Effect |
|---|---|
| **News window (days)** | Only articles published within this window are considered. 1–2 for a tight daily read, 7 for catching up. |
| **Max stories per section** | Longer report, more tokens. 3–5 is the sweet spot. |
| **Sections to include** | Deselecting a section skips its searches *and* its writer, so it genuinely saves time. |

Settings apply to the next generation. The current report is held in memory
(`st.session_state`) so changing a slider doesn't re-bill you — press
**Generate** when you want a new one.

---

## Tuning

All knobs live in `.env` (see `.env.example`):

| Variable | Default | Meaning |
|---|---|---|
| `GROQ_MODEL` | `openai/gpt-oss-20b` | Writer model |
| `CRITIC_MODEL` | same | Editor model |
| `REASONING_EFFORT` | `low` | Reasoning budget for gpt-oss / qwen3 models |
| `NEWS_WINDOW_DAYS` | `2` | Default news window |
| `MAX_STORIES_PER_SECTION` | `5` | Default stories per section |
| `MAX_CANDIDATES_PER_SECTION` | `7` | How many stories a writer may choose from |
| `MAX_REVISIONS` | `1` | Max rewrite rounds per section |
| `LLM_CONCURRENCY` | `2` | Parallel model calls (lower it if you hit 429s) |
| `LLM_MAX_TOKENS` | `4000` | Output budget per call |
| `LLM_TIMEOUT` | `60` | Seconds before a stalled model call is abandoned |
| `MAX_FETCH_CHECKS` | `4` | Pages fetched per section for claim checking |

If you hit Groq rate limits, drop `LLM_CONCURRENCY` to `1` and reduce
`MAX_STORIES_PER_SECTION`.

---

## Source policy

* **Tier 1 (preferred):** official company and lab blogs — OpenAI, Google
  DeepMind, Anthropic, NVIDIA, Microsoft, Meta, Hugging Face, arXiv, and similar.
* **Tier 2:** credible independent reporting — Reuters, TechCrunch, The Verge,
  Ars Technica, Wired, IEEE Spectrum, Nature, and similar.
* **Blocked as primary citations:** social media, aggregators, Medium, Reddit,
  Pinterest, Quora.
* **Structured sources:** arXiv (research), GitHub search (open source),
  Hacker News (early developer signal — weighted lower on purpose).

A story covered by several independent outlets gets a coverage bonus, because
independent corroboration is real evidence of importance.

---

## Known limitations

* Free-tier LLM rate limits are the main failure mode. The pipeline retries with
  exponential backoff, but a very aggressive configuration can still stall.
* Verification is structural and textual. It catches invented links and invented
  numbers; it cannot catch a subtly wrong interpretation of a true sentence.
* Paywalled pages often cannot be fetched, so claim spot-checks are skipped for
  them (this is logged, not hidden).
* Sections with no qualifying news say so in one honest sentence rather than
  padding with filler.

---

## Built with

Streamlit · LangGraph · LangChain · Groq · Tavily · Pydantic · trafilatura ·
BeautifulSoup · pandas · arXiv · GitHub · Hacker News

---

<sub>Capstone project by **Rohit Jha**. Built for daily personal use.</sub>
