# Aether — Showcase Guide

Everything you need to *present* this project for internships, GitHub, LinkedIn
and interviews. This file is for you — recruiters never see it.

---

## 1. The one-liner (use this everywhere)

> **Aether** is a multi-agent AI workplace: a Planner agent routes each request
> to a **PDF Document Analyst** (RAG with FAISS + page-cited answers) and a
> **live web Researcher**, then a Writer agent packages everything into a
> cited, structured report. Ships with a **deterministic evaluation harness**
> (hit@k / MRR / LLM-judged groundedness), a pytest suite and CI.

## 2. Resume bullets (copy-paste, tune the numbers if you re-run eval)

- Built **Aether**, a multi-agent research assistant (LangChain 1.x, Groq,
  FAISS, Streamlit) featuring a **Planner-Executor architecture** where an LLM
  routes each request between RAG-based document analysis and live Tavily web
  search.
- Engineered a **RAG pipeline** (pypdf → recursive chunking 1000/150 →
  MiniLM embeddings → FAISS) preserving **page-level provenance**, enabling
  source-cited answers; achieved **100% retrieval hit@4** and **MRR of 0.786** on a
  golden-QA evaluation set.
- Implemented **LLM-as-judge evaluation** measuring groundedness and refusal
  behaviour (the assistant refuses out-of-document questions), plus a
  **stubbed router unit test** validating planner tool-selection accuracy.
- Added **error-tolerant tool middleware** so a failing tool degrades a session
  instead of crashing it, and a **pytest + GitHub Actions CI** pipeline that
  runs keyless tests on every push.

Fill X/Y from `evaluation/RESULTS.md` after your latest run.

## 3. Demo script (90 seconds)

1. **Open with the diagram** (`assets/architecture.png`): "One planner, three
   specialists, one writer."
2. Upload `sample_data/Aether_Product_Handbook.pdf` (bundled — zero setup).
3. Ask: *"What chunk size and overlap does the splitter use?"* → answer cites
   the page. Point at the metrics panel (pages / chunks / vectors).
4. Ask: *"Who won the 2022 FIFA World Cup?"* → it **refuses** — say: "This
   gatekeeping is deliberate; hallucination is a feature-killing bug."
5. Ask: *"Does the handbook cover middleware, and add current industry context
   on agent reliability?"* → both agents run; show the `st.status` trace, then
   the structured report.
6. Finish: "The numbers aren't vibes — there's an eval harness in the repo."

**Record this as a GIF** (e.g., ScreenToGif) → `assets/demo.gif` → embed it at
the top of the README. Projects with a demo GIF get dramatically better
engagement. Optional: 2–3 screenshots in `assets/screenshots/`.

## 4. LinkedIn post (template)

> 🚀 Capstone Project: **Aether — my multi-agent AI workplace**
>
> Most "chat with your PDF" demos stop at retrieval. I wanted to know whether
> mine actually works — so I built evaluation into the product.
>
> What Aether does:
> ✅ Planner agent routes each question (PDF? web? both?)
> ✅ Document Analyst answers **only** from your PDF — with page citations
> ✅ Researcher brings in live web context (Tavily)
> ✅ Writer formats everything into a structured report
> ✅ Evaluation harness: hit@k, MRR, LLM-judged groundedness, refusal tests
> ✅ pytest + GitHub Actions CI
>
> Hard lesson: agents fail gracefully only if you design the failure path —
> every tool call in Aether is wrapped by error-handling middleware.
>
> 👉 Repo: [link] · Demo: [link]
>
> #GenAI #LangChain #RAG #FAISS #LLM #Python #OpenToWork

Even better: post a 60s screen-recording instead of text-only.

## 5. GitHub checklist (do these before sharing)

- [x] README with architecture diagram, quickstart, evaluation table
- [x] `requirements.txt`, `.env.example`, `.gitignore`, LICENSE (MIT)
- [x] Tests + CI badge (add the badge after first push — URL below)
- [x] Sample data so anyone can run it in 2 minutes
- [ ] **Make Aether its own repo** (currently it lives inside a big folder).
      ```powershell
      cd "...AI and Data Science\...\Aether"
      git init
      git add .
      git commit -m "Aether: multi-agent AI workplace with RAG evaluation"
      git remote add origin https://github.com/<you>/Aether.git
      git push -u origin main
      ```
- [ ] Pin it on your profile ("Popular repositories")
- [ ] Add the CI badge to the README top:
      `![CI](https://github.com/<you>/Aether/actions/workflows/tests.yml/badge.svg)`
- [ ] Record `assets/demo.gif`
- [ ] (Optional) Deploy free on Streamlit Community Cloud — put the app URL
      in the README header. Store Groq/Tavily keys as Streamlit secrets.

## 6. Interview questions you should be able to answer

1. **Why Planner-Executor instead of one prompt?** → routing between document
   facts and web facts; separation of collection vs. formatting.
2. **How do you prevent hallucination?** → strict analyst prompt, top-4
   retrieval, refusal behaviour — and you *measure* it (judge evaluates
   `grounded` / `out_of_context` / `refused`).
3. **What would you improve first?** → streaming, OCR for scanned PDFs,
   hybrid retrieval (BM25 + dense), persistent multi-doc index.
4. **Why FAISS over Pinecone?** → single-doc session workload, zero hosting,
   session-lifetime data.
5. **How do you know chunk size 1000/150 is right?** → the harness exists;
   re-run it with different parameters and compare tables (that's the honest
   answer, and it shows engineering maturity).

## 7. Portfolio positioning

For a first internship, this project demonstrates: LLM orchestration, RAG
engineering, evaluation methodology, DevOps hygiene (tests + CI), and
product thinking (bundled sample data, one-liner pitch). That combination is
exactly what "AI engineer intern" roles screen for.
