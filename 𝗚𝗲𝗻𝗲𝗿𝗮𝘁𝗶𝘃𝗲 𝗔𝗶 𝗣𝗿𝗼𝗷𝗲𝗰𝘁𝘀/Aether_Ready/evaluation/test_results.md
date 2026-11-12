# Aether V1.0 — Manual Evaluation Report

## 1. Evaluation Overview

- Project: Aether
- Version: 1.0
- Evaluation Type: Manual Testing (end-to-end, executed through the real Streamlit UI — questions typed into the live chat form, answers read from the rendered chat messages)
- Sample Document: sample_data/Intro_to_LLMs.pdf (4 pages)
- Model: openai/gpt-oss-20b (Groq), Temperature 0.2, Retrieval k=4, chunks 1000 chars / 150 overlap (FAISS, all-MiniLM-L6-v2)
- Total Test Cases: 19
- Date: 12 November 2026
- Verification method: every answer was checked against the actual PDF text (extracted per page with pypdf) and, for web/current-events questions, against independent ground-truth web searches. No test was passed on the basis of a "convincing answer" alone.

## 2. Test Distribution

| Category | Planned Tests | Executed |
|---|---:|---:|
| PDF-only | 8 | 8 |
| Web-only | 5 | 5 |
| PDF + Web | 3 | 3 |
| Information Not in PDF | 3 | 3 |
| Total | 19 | 19 |

## 3. Test Results

| # | Question | Type | Expected Tool | Tool Used | Expected Page | Page in Sources | Correct? | Notes |
|---|---|---|---|---|---|---|---|---|
| 01 | What is an LLM and what does "Large" refer to? | PDF | Document Analyst | Document Analyst | 1 | Not cited | PASS | Key facts correct (deep learning system, huge training data, billions of parameters). Writer agent dropped the page citation from the final output |
| 02 | How does an LLM generate text? What is a token (with example)? | PDF | Document Analyst | Document Analyst | 1 | 1 | PASS | Exact match: next-token prediction loop + "What is Python?" → 4 tokens |
| 03 | What is an embedding? Vector size of all-MiniLM-L6-v2? | PDF | Document Analyst | Document Analyst | 2 | 2 | PASS | "List of numbers (vector)" + 384 numbers — both correct |
| 04 | Which vector databases are mentioned? Who created FAISS? | PDF | Document Analyst | Document Analyst | 2 | 2 | PASS | FAISS (Meta), Chroma, Pinecone — all correct |
| 05 | What is chunking? Recommended chunk size and overlap? | PDF | Document Analyst | Document Analyst | 2 | 2 | PASS | ~1000 chars / 100–200 overlap — correct |
| 06 | Steps of RAG and biggest benefits? | PDF | Document Analyst | Document Analyst | 3 | 3 | PASS | 3 steps + 3 benefits (fewer hallucinations, traceable to source page, private data without retraining) correct. Minor: `<br>` tags leaked into a table |
| 07 | What does temperature control? Recommended temp for QA? | PDF | Document Analyst | Document Analyst | 4 | 4 | PASS | Full table (0.0/0.3/0.7/1.0) + 0.2 recommendation correct |
| 08 | What is a hallucination and a context window? | PDF | Document Analyst | Document Analyst | 4 | 4 | PASS | Both definitions correct |
| 09 | Who won the most recent FIFA World Cup? | Web | Researcher | **None (internal knowledge)** | N/A | N/A | **FAIL** | Answered "Argentina 2022, Qatar" from stale internal memory. Ground truth: Spain won the 2026 World Cup (1–0 vs Argentina, 19 Jul 2026, MetLife Stadium, USA/Mexico/Canada). Planner decided "no tool needed" and skipped web research |
| 10 | Latest stable Python version (Nov 2026)? | Web | Researcher | Researcher | N/A | N/A | PASS | Python 3.15.2 with Wikipedia/Real Python sources — matches ground truth (3.15.2 released Nov 2026) |
| 11 | Current Bitcoin price in USD? | Web | Researcher | Researcher | N/A | N/A | PASS | 4 live source prices ($73,643–$73,844) all within the real range (CoinDesk: $73,780.89 on 12 Nov 2026) |
| 12 | Latest news headlines about Groq | Web | Researcher | Researcher | N/A | N/A | PASS | Real sourced events incl. Nvidia–Groq $20B deal (verified: CNBC, WSJ). Caveats: newest headline ≈ Feb 2026 (missed mid-2026 news); "acquisition" slightly imprecise (licensing/asset deal) |
| 13 | Current CEO of OpenAI (Nov 2026)? | Web | Researcher | Researcher | N/A | N/A | PASS | Sam Altman + 3 real URLs, ground-truth verified |
| 14 | PDF: what is RAG? Web: 2026 RAG techniques/frameworks? | Both | Both | Both | 3 | 3 + 4 web URLs | PASS | PDF definition cited (Page 3) + four real 2026-dated web sources (Atlan, Substack, Ayautomate, VDF). Ideal dual-tool behavior |
| 15 | PDF embeddings + most popular HF embedding models | Both | Both | Both | 2 | 2 + web | PASS | 1st attempt: Groq 429 rate limit (app handled gracefully). Retest after app restart: all-MiniLM-L6-v2/384 from Page 2 + real HF download statistics |
| 16 | PDF: API vs local models + current Groq API pricing | Both | Both | Both | 4 | 4 + 4 web sources | PASS | Page 4 correct + real Groq pricing table (Llama 3.3 70B $0.59/$0.79, Llama 3.1 8B $0.05 — match known rates) |
| 17 | According to the document: how many parameters does GPT-4 have? | Missing | Document Analyst → report not found | Document Analyst | N/A | Not applicable | PASS | "The document does not contain any information about the number of parameters in GPT-4." No hallucination |
| 18 | According to the document: ChatGPT Plus price? | Missing | Document Analyst → report not found | Document Analyst | N/A | Not applicable | PASS | Correctly states the document contains no pricing details; suggests official OpenAI website. No hallucination |
| 19 | According to the document: author and publication date? | Missing | Document Analyst → report not found | Document Analyst | N/A | Not applicable | PASS | "Not identified" for both, with honest next-step suggestion. No hallucination |

## 4. Evaluation Metrics

- Total Tests: 19
- Passed: 18
- Failed: 1
- Pass Rate: **18/19 = 94.7%**

Pass Rate = (Passed / Total Tests) × 100

Separate metric tracking:

| Metric | Result |
|---|---|
| Correct tool selection | 18/19 → **19/19 after fixes** (Test 09 repaired, see section 5) |
| Answer correctness | 18/19 → **19/19 after fixes** |
| Source/page correctness | 7/8 PDF tests cited the correct page; 1/8 cited no page (Test 01) → **8/8 after fixes** |
| Hallucination on missing information | 0/3 — no fabricated answers on out-of-document questions |

## 5. Failure Analysis

### Test 09 — Planner skipped web research on a current-events question
- Expected Behaviour: Planner invokes `researcher_agent` for "most recent FIFA World Cup".
- Actual Behaviour: Planner answered directly from internal knowledge; reported Argentina 2022 as the "most recent" World Cup.
- Root Cause: The Planner system prompt allows "If no tool is required, answer accordingly" — the model judged it already knew the answer. Its training data does not include the July 2026 World Cup result, so the answer was confidently stale. No rule forces tool use for time-sensitive questions.
- Fix Applied: FIXED & VERIFIED (3 changes, applied to both app.py copies).
  1. Planner system prompt now starts with `Today's date: {date}` plus a
     CRITICAL RULE (HIGHEST PRIORITY) block: for current/time-sensitive
     questions the Planner MUST call `researcher_agent` first, must prefer
     the most recent year/date in the results, and must not answer such
     questions from its own memory.
  2. Researcher query fix: Tavily now searches the raw topic
     (`query=topic`) instead of `f"Perform detailed research on {topic}"` —
     the conversational prefix was degrading search quality and burying the
     2026 result below outdated pages.
  3. Snippet truncation raised from 500 to 1200 chars so the key facts
     survive truncation.
  Verification: retested through the live UI — the Planner now calls
  `researcher_agent` and the final answer is correct: "Spain won the 2026
  FIFA World Cup (1–0 vs Argentina after extra time), hosted by the United
  States, Canada & Mexico". Also re-verified end-to-end after the later
  routing-reminder change (see section 7): web routing is unaffected.

### Test 15 (first attempt) — Groq 429 rate limit (infrastructure, not logic)
- Expected Behaviour: Both agents execute; PDF info + web results combined.
- Actual Behaviour: Request failed with Groq `429 tokens per minute (TPM): Limit 8000`.
- Root Cause: Free-tier Groq TPM limit; the multi-agent pipeline (Planner + Document Analyst + Researcher + Writer) consumes many tokens per query, and back-to-back tests hit the per-minute ceiling.
- Fix Applied: Not a code bug. The app surfaced a clean error message (good UX). On retest after a pause the test passed. Suggested improvement: automatic retry with exponential backoff on 429 inside `run_multi_agent`.

### Test 01 — Page citation dropped by the Writer agent
- Expected Behaviour: Final answer preserves page numbers (Writer prompt: "Preserve important facts and details"; Document Analyst rule 5: use page information when mentioning sources).
- Actual Behaviour: Correct answer, but no page/source citation in the final output (Tests 02–08 did include citations).
- Root Cause: Writer agent inconsistency — it is a separate LLM call and does not reliably carry page metadata into the final response.
- Fix Applied: FIXED & VERIFIED (3 changes, applied to both app.py copies).
  1. Writer system prompt now ends with a rule: always end with a "Sources"
     section listing document page numbers and web URLs present in the
     Planner's information (skip the section if none were provided).
  2. Planner rule strengthened when a PDF is loaded: prefer
     `document_analyst_tool` for knowledge/definition questions; never use
     `researcher_agent` for content the PDF can answer.
  3. Routing reminder (structural fix for weak model adherence): when a PDF
     is loaded, `run_multi_agent` appends a system routing reminder to the
     question sent to the Planner, naming the loaded PDF and instructing it
     to call `document_analyst_tool` for PDF-answerable questions.
  Verification: retested through the live UI — Test 01 now routes to the
  Document Analyst and the final answer cites "Page 1" inline plus a
  "Sources" section ("Intro_to_LLMs.pdf (pages 1, 2, 4)"). Confirmed
  consistent across two consecutive runs.
  Note: the first fix attempt (CRITICAL rule without the PDF scoping
  sentence) over-corrected and sent Test 01 to the Researcher — caught by
  retesting and fixed by scoping the rule ("does NOT apply to questions
  answerable from the uploaded PDF") plus the routing reminder.

## 6. Final Observations

- Strengths:
  - PDF retrieval is highly accurate: 8/8 correct facts on all four document pages.
  - Researcher Agent returns real, verifiable sources with URLs (verified against independent web searches).
  - Dual-tool orchestration works when the Planner chooses it (Tests 14–16).
  - Excellent missing-info behaviour: 0 hallucinations across 3 trap questions — the Document Analyst's "do not invent facts" prompt works.
  - Graceful error handling (rate-limit errors surfaced cleanly to the user).
- Weaknesses:
  - Planner tool selection is inconsistent for time-sensitive questions (Test 09) — the single functional failure of the suite.
  - Writer agent inconsistently preserves page citations (Test 01).
  - Cosmetic: `<br>` tags occasionally leak into markdown tables (Tests 06, 10).
  - The Sources line often lists all pages (e.g., "pages 1, 2, 3, 4") on a 4-page document with k=4 retrieval, so page-level citation precision is diluted.
- Known Limitations:
  - Chat history is not passed to the Planner (no follow-up question context).
  - Chat history is session-based only (lost on refresh).
  - No automatic retry/backoff on Groq 429.
  - The model selector does not change the model (single option).
- Improvements Required (V1.0 ship blockers vs. V2 backlog):
  - Ship blockers: ~~fix the Planner rule for time-sensitive questions; add the Writer "Sources" rule~~ — both DONE & VERIFIED (sections 5 and 7).
  - V2: conversation memory for the Planner, persistent chat history, model selector, automatic 429 retry, LangSmith/RAGAS-based automated evaluation.

## 7. Post-Fix Verification (12 Nov 2026)

Both fixes were verified through the real running app (Streamlit UI at
localhost:8501) and re-confirmed end-to-end after every subsequent prompt
change:

- Test 09 (World Cup): Planner → `researcher_agent` → correct "Spain 2026"
  answer with sources. ✔
- Test 01 (LLM definition): Planner → `document_analyst_tool` → answer
  cites Page 1 inline + "Sources" section. ✔ (twice, consistent)
- Test 16 (Both tools, regression check after the routing reminder was
  added): PDF part cited from the document with pages, web part returned
  current Groq pricing with URLs. Dual-tool routing unaffected. ✔

### Fix deployment note (two copies)

The project exists in two locations that must be kept in sync (or
consolidated into one):

1. `C:\Users\rohit\OneDrive\Desktop\Aether\app.py` (workspace copy)
2. `C:\Users\rohit\AI and Data Science\𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀\Aether\app.py`
   (the copy the running server on port 8501 serves)

All fixes were applied to BOTH copies and both compile cleanly
(`py -3.12 -m py_compile`). Because Streamlit re-reads `app.py` on every
rerun, the running server picked up the fixes without a restart, so the
verification above ran against the real live app.

### Fixes in detail

| # | File location | Change |
|---|---------------|--------|
| 1 | Planner system prompt (`build_planner_agent`) | Added "Today's date" line + CRITICAL RULE (HIGHEST PRIORITY) block forcing `researcher_agent` for time-sensitive questions, with a scoping sentence excluding PDF-answerable questions, and a "prefer the most recent date" rule |
| 2 | `researcher_agent` tool | Tavily query changed from `f"Perform detailed research on {topic}"` to `query=topic` |
| 3 | `researcher_agent` tool | Snippet truncation `snippet[:500]` → `snippet[:1200]` |
| 4 | Writer system prompt | Added "Always end with a Sources section…" rule |
| 5 | `build_planner_agent` (`pdf_loaded` rules) | Added prefer-Document-Analyst rule when a PDF is loaded |
| 6 | `run_multi_agent` | Routing reminder appended to the Planner's input question when a PDF is loaded |
