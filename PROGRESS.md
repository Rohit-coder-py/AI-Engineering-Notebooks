# 🚀 Harsh's 6-Month AI Engineering Roadmap — Progress Tracker

> **Started:** 12 May 2026 (Monday)
> **Roadmap length:** 24 weeks (6 months × 4 weeks)
> **Status as of:** 9 Nov 2026 (~26 weeks in)
> **Current position:** Month 5 — Week 4 (GenAI & LLMs, deployment week)
> **Pace:** ~1 month behind schedule → on current pace, Month 5 finishes ~mid-Dec, then Month 6 (Job Prep)

---

## 📊 Overall Dashboard

| Month | Focus | Status | Period | Evidence in this folder |
|-------|-------|--------|--------|------------------------|
| 1 — Python | Python, NumPy, Pandas, EDA, Viz | ✅ **DONE** (ahead of plan) | ~May–Jun | 𝗗𝗮𝘁𝗮 𝗔𝗻𝗮𝗹𝘆𝘀𝗶𝘀 𝗮𝗻𝗱 𝗩𝗶𝘀𝘂𝗮𝗹𝗶𝘇𝗮𝘁𝗶𝗼𝗻 (NumPy, Pandas, Matplotlib, Seaborn, Plotly, EDA notes), 𝗗𝗦𝗔, 𝗦𝘁𝗿𝗲𝗮𝗺𝗹𝗶𝘁 |
| 2 — Mathematics | Stats, Probability, Linear Algebra, Calculus | ✅ **DONE** | ~Jun–Jul | 𝗠𝗮𝘁𝗵𝗲𝗺𝗮𝘁𝗶𝗰𝘀 (Linear Algebra notebooks, Statistics & Probability PDF, Calculus / Differentiation / Integration) |
| 3 — Core ML | Regression → Trees → Clustering | ✅ **DONE + bonus** | ~Jul–Aug | 𝗠𝗮𝗰𝗵𝗶𝗻𝗲 𝗟𝗲𝗮𝗿𝗻𝗶𝗻𝗴 (notebooks: train/test split, encoding, scaling, tuning, CV, model saving) + **10 ML projects** |
| 4 — Deep Learning | PyTorch, ANN/CNN/RNN, NLP, Transformers | ✅ **DONE + bonus** | ~Aug–Oct | 𝗗𝗲𝗲𝗽 𝗟𝗲𝗮𝗿𝗻𝗶𝗻𝗴 (notes + Transformers) + 𝗗𝗲𝗲𝗽 𝗟𝗲𝗮𝗿𝗻𝗶𝗻𝗴 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀 (ANN/CNN/RNN/Transformers) + 𝗡𝗟𝗣 notes & projects |
| 5 — GenAI & LLMs | LLMs, RAG, Agents, Deployment | 🟡 **IN PROGRESS — Week 4** | Oct–now | 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 (01_LLM Foundations, 02_RAG, 03_AI Agents) + 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀 + 𝗙𝗮𝘀𝘁𝗔𝗣𝗜 + 𝗣𝘆𝗱𝗮𝗻𝘁𝗶𝗰 |
| 6 — Job Prep | Resume, LinkedIn, Interviews | ⬜ **NOT STARTED** (starts ~Nov 12) | next | — |

**Legend:** ✅ done · 🟡 in progress · ⬜ not started

---

## ✅ Month 5 — Generative AI & LLMs (week-by-week)

| Week | Topics | Status | Your evidence |
|------|--------|--------|---------------|
| W1 — LLM basics, prompting | API calls, system prompts, few-shot | ✅ Done | `𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶\01_LLM Foundations` (chat models incl. HuggingFace local, embeddings, ChatPromptTemplate, AI CHATBOT, EDUSAGE AI v2) + `Multi Lingular AI Chatbot` ✅ roadmap project done |
| W2 — RAG | Embeddings, vector DBs, chunking, retrieval | ✅ Done | `02_RAG` (document loaders, text splitters incl. semantic, Vector DBs, retrievers incl. MultiQuery/MMR) + `Ask-Your-PDF` + `Krishi Mitra AI` + `BankSaathi AI` |
| W3 — Agents | Tool calling, ReAct, memory, multi-tool | ✅ Done | `03_AI Agents` (Tools in LangChain incl. Tavily search + custom tools, Runnables sequence/parallel, multi agent system, City Assistant AI Agent) + `Flipkart Shopping Assistant` + `Aether` + `omnirouter` |
| W4 — Deployment | FastAPI, Pydantic, Docker, Spaces | 🟡 In progress | `𝗙𝗮𝘀𝘁𝗔𝗣𝗜` (4 modules done), `𝗣𝘆𝗱𝗮𝗻𝘁𝗶𝗰` (6 modules done) · ⬜ Docker · ⬜ Deploy on Spaces · ⬜ Final capstone: deployed AI support bot (FastAPI + Streamlit + RAG) |

### Deployment reality check ✅ (verified from READMEs on 2026-11-09)
Wrong assumption corrected: the deployment habit is **already strong**. Verified live links across READMEs:

| Already deployed & live | |
|---|---|
| Full API architecture ⭐ | **Fake Job Posting Detection System** — FastAPI backend on **Render** + Streamlit frontend (https://fake-job-posting-detection-system.onrender.com) |
| GenAI deployed | **Ask-Your-PDF** (RAG) · **Multi Lingular AI Chatbot** (llm-chatbot-genai.streamlit.app) |
| FastAPI apps | **Facial Emotion Recognition** (facial-emotion-recognition-fastapi.streamlit.app) |
| DL/ANN live apps | Customer Churn · Credit Card Fraud · Medical Insurance Cost · Smartphone Addiction · ShipSense v2 |
| CNN | Indian Food Classifier · Chest X-Ray Pneumonia · Cat-vs-Dog |
| RNN/Transformers | Sentence Auto Completer (LSTM from scratch) · AI Text Summariser (distilbart) |
| NLP | Customer Support Ticket Classification · ChatGPT Sentiment Analysis |
| ML | AI Cloud Cost Predictor · Employee Attrition · Retail Customer Segmentation · Shipping Delay (ShipSense dashboard) |

~19 unique live apps.

### 🔜 Month 5 remaining checklist
- [ ] Finish FastAPI: serving models, API testing
- [ ] Docker basics (Dockerfile for a FastAPI app) ← main gap
- [ ] Deploy **BankSaathi AI** — README still has `your-app-name.streamlit.app` placeholder ("TO DO AFTER DEPLOYING")
- [ ] Deploy remaining GenAI apps: Krishi Mitra AI · Flipkart Shopping Assistant · Aether
- [ ] 🔐 Confirm: no API keys in code — all in `.env` / environment variables
- [ ] ⭐ Bonus resources you already have ahead of Month 6: SQL notes + 3 SQL projects (Month 6 Week 3 covered!)

---

## 🏆 Portfolio Inventory (what you can put on the resume TODAY)

> Roadmap asks for ~3 deployed projects. You have ~30 built. These are resume-eligible:

### GenAI / LLM (Month 5) — strongest differentiators
| Project | Type | Roadmap equivalent | Status |
|---------|------|-------------------|--------|
| Krishi Mitra AI | RAG (agriculture assistant) | Constitution Q&A bot ✅ | Built — deploy it |
| Ask-Your-PDF | RAG (chat with PDF) | — bonus | ✅ **Deployed** (ask-your-pdf-genai.streamlit.app) |
| BankSaathi AI | RAG (bank support, multilingual) | Support bot ✅ | Built — deploy it (README placeholder pending) |
| Multi Lingular AI Chatbot | LLM app (multilingual) | Multilingual chatbot ✅ | ✅ **Deployed** (llm-chatbot-genai.streamlit.app) |
| Flipkart Shopping Assistant | Agent / tool calling | Startup research agent ✅ | Built — deploy it |
| City Assistant AI Agent | Multi-tool agent | — bonus | Built |
| Aether / omnirouter | LLM router / agent | — bonus | Built |

> ⭐ Deployment is verified across **19 live apps** — see the "Deployment reality check" section above. This already exceeds the roadmap's "3 deployed projects" resume bar.

### Machine Learning (Month 3) — 10 projects
Heart Disease Predictor · Loan Approval Predictor · Employee Salary Predictor · AI Cloud Cost Prediction · Retail Customer Segmentation (K-Means ✅ roadmap project) · Shipping Delay Prediction · Student Score Predictor · Students Success Predictor · Employee Attrition & HR Analytics · AI Resume Screening & Candidate Ranking

### Deep Learning (Month 4) — 11 projects
- **ANN:** Customer Churn · Credit Card Fraud Detection ✅ (roadmap M3W3) · Medical Insurance Cost · Smartphone Addiction · ShipSense v2
- **CNN:** **Indian Food Image Classifier (EfficientNet)** ✅ exact roadmap Month 4 Week 2 project · Cat-vs-Dog · Chest X-Ray Pneumonia
- **RNN/Transformers:** Sentence Auto Completer · Free Fire Review Sentiment · AI Text Summariser

### NLP
Chatgpt Sentiment Analysis · Customer Support Ticket Classification — pair with roadmap M4W3 (fake news / BERT fine-tune) if you want the exact box ticked

### SQL (Month 6 W3 — already done)
Students Management · Library Management · E-Commerce DB (with views, ER diagrams, reports)

---

## ⏰ Timeline math

- On schedule, Month 5 would have ended ~12 Oct 2026; you're ~4 weeks behind on the calendar.
- **Reality check:** depth is way ahead of schedule — roadmap expects ~5 GenAI projects total by Month 5's end; you've built 7, plus 21 DL/ML projects.
- Current finish line for all 6 months: **~mid-Jan 2027** if Weeks 4–6 go at normal pace. To finish by the original mid-Nov-Dec plan, compress Month 6 to 3 weeks (very doable — SQL is already done).

---

## 🎯 Next 3 moves (updated after deployment audit)

1. **Deploy BankSaathi AI + finish Docker this week** — it's the last open Week 4 items. (You've already cracked the hard part: a FastAPI backend is live on Render via Fake Job Posting Detector.)
2. **Write metrics into every README** — "achieved Z" numbers are what the resume format needs. Even simple: accuracy, F1, retrieval hit-rate, avg response time.
3. **Start applying NOW, don't wait for Month 6** — the roadmap's own tip says start from Month 4. With ~19 live apps + Month 5 nearly done at 17 years old, the ₹8–14 LPA mid-tier column is a realistic target from ~Dec.

---

## 📓 Progress Log (append new entries at the bottom)

| Date | Event |
|------|-------|
| 2026-05-12 | Roadmap started |
| 2026-11-08 | Made first detailed progress audit. Confirmed: M1–M4 done, M5 at Week 4 (FastAPI/Pydantic in progress, Docker/deployment pending). Tracker created. |
| 2026-11-09 | Session note: confirmed LangChain learned, building projects. |
| 2026-11-09 | Deployment audit after Harsh's correction: ~19 live apps verified in READMEs (Streamlit + 2 FastAPI incl. Render backend). Tracker updated — deployment is NOT the gap; Docker + BankSaathi/3 GenAI deploys are. |

---

*How to use this file: whenever you finish a checkbox, tell me (or edit it yourself) and I'll update the dashboard + log. New month → new section. Keep the log row count honest — this file doubles as your Month 6 resume raw material.*
