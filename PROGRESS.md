# 🎯 Pre-Month-6 Gap Tracker

> **Purpose:** Everything left to close before starting Month 6 (Job Prep + 3 Capstones).
> Based on a full audit of this repo against the 6-Month AI Engineering Roadmap (audited on 2026-11-10).
>
> **Rule:** Tick a box only when there's a **file in this repo** proving it.

---

## 📊 Where I Stand Right Now

| Month | Skills/Concepts | Assigned Projects | Verdict |
|:---:|:---|:---|:---|
| 1 — Python | ✅ NumPy/Pandas/Matplotlib/Seaborn notes | ❌ 0 of 5 in repo | 🟡 Partial |
| 2 — Mathematics | 🟡 Bayes + LA + derivative theory | ❌ 0 of 4 as specified | 🟡 Partial |
| 3 — Core ML | ✅ Strong (Ml Topics + master notebook) | 🟡 1 of 4 as specified | 🟡 Mostly done |
| 4 — Deep Learning | ✅ Strongest month | 🟡 1 of 4 exact + several substitutes | ✅ Nearly done |
| 5 — GenAI & LLMs | ✅ Very deep (RAG, agents, FastAPI, pytest+CI) | 🟡 W1 & W2 shipped via own projects | ✅ Nearly done |

**Estimated time to close all gaps: ~9–10 focused days.**

---

## 🔥 Tier 1 — Interview-Critical (do first, ~3–4 days)

### ☐ 1. Gradient Descent From Scratch — Month 2, Week 4
- [ ] Pure NumPy implementation (no sklearn, no autograd)
- [ ] Fit a straight line to data (y = w·x + b, updated via w -= lr * dL/dw)
- [ ] Plot **error vs epoch** decreasing
- [ ] Try 3 learning rates (0.001 / 0.1 / 1.0) and screenshot the diverging one
- [ ] Write 3 observations in plain English under the plot
- **Where:** `Mathematics/Calculus/06_gradient_descent_from_scratch.ipynb`
- **Why:** The #1 fresher ML interview question. Roadmap tip: "Do not skip it."

### ☐ 2. Loan Approval Predictor — Imbalance Upgrade — Month 3, Week 2
Current state: `ML Projects/Loan Approval Predictor` has no imbalance handling.
- [ ] Add SMOTE or `class_weight='balanced'`
- [ ] Plot confusion matrix (heatmap, not text print)
- [ ] Plot ROC-AUC curve
- [ ] Plot **Precision-Recall curve** (the roadmap's actual focus)
- [ ] Add a README section: "Why accuracy alone is misleading here" with before/after numbers
- **Why:** Precision-recall tradeoff on imbalanced data is an interview staple. I already wrote this argument in the Fake Job Posting README — now back it with plots.

### ☐ 3. Ensemble Comparison Project — Month 3, Week 3
Current state: no sklearn Tree/RF/XGBoost comparison exists (my fraud project is the PyTorch ANN version).
- [ ] Credit card fraud dataset → Decision Tree vs Random Forest vs XGBoost
- [ ] Print + plot `feature_importances_` for the winner
- [ ] Add k-fold cross-validation (`cross_val_score`, cv=5)
- [ ] One-paragraph conclusion: which model and why
- **Where:** new repo `Credit-Card-Fraud-ML-Ensembles`
- **Why:** "What's feature importance?" is asked in every ML interview.

---

## 🔥 Tier 2 — Capstone Blockers (~5–6 days)

### ☐ 4. One Real BERT Fine-Tune — Month 4, Week 3
Current state: DistilBART summariser is inference-only; no fine-tuning of any LLM.
- [ ] Use HF `Trainer` + `TrainingArguments` (not a manual loop) on `distilbert-base-uncased`
- [ ] Dataset: reuse existing ChatGPT-sentiment data
- [ ] Evaluate: F1 score, compare vs the TF-IDF baseline notebook
- [ ] Save tokenizer + model, load in a Streamlit app
- [ ] (Stretch) multilingual BERT variant with per-language F1
- **Why:** "Have you fine-tuned a model?" — the answer must be yes, not "I read about it."

### ☐ 5. FastAPI RAG Backend + API Tests — Month 5, Week 4 + the API-testing gap
- [ ] Wrap Krishi Mitra **or** BankSaathi RAG chain in FastAPI: `POST /chat`
- [ ] Pydantic request/response models (`question: str`, `answer: str`, `sources: list`)
- [ ] `.env.example` + `load_dotenv()` — no keys in code
- [ ] `tests/test_api.py` using **FastAPI TestClient** (~the roadmap's "API testing"):
  ```python
  from fastapi.testclient import TestClient
  def test_chat_returns_answer():
      res = client.post("/chat", json={"question": "What is the repo rate?"})
      assert res.status_code == 200
      assert "answer" in res.json()
  ```
  Cover: 200 OK, 422 invalid body (missing field), 500-safe behavior on empty index
- [ ] Run `pytest tests/ -v` clean, add to CI like Aether
- **Tool note:** roadmap says "API testing" → pytest + TestClient, **not Postman** (Postman = optional GUI exploration only)

### ☐ 6. Docker That Actually Works — Month 5, Week 4
Current state: `Generative AI/Docker/Dockerfile` is **empty**; Krishi Mitra README promises a Dockerfile that doesn't exist.
- [ ] Containerize the Tier-2 FastAPI bot (item 5): real Dockerfile, `docker build`, `docker run`, hit the endpoint from a browser → screenshot proof
- [ ] Or if skipping Docker: **remove the dangling Docker claims** from READMEs
- **Why:** One leaked/false claim in a README is worse than one missing feature.

---

## ⬜ Tier 3 — Polish (half-day each, in any order)

### ☐ 7. Few-Shot Prompting Notebook — Month 5, Week 1
- [ ] One task, 3 variants: zero-shot vs 3-shot vs 5-shot, same example questions
- [ ] Note output differences

### ☐ 8. MNIST Train-vs-Val Loss Plot — Month 4, Week 1
- [ ] In `Deep Learning/Notes/Deep Learning Notes.ipynb` MNIST section: add validation split, collect val loss per epoch, plot both curves in one matplotlib figure

### ☐ 9. Manual Bayes Spam Counter — Month 2, Week 2
- [ ] Median short notebook (~50 lines): count word frequencies per class by hand, compute P(spam|word) manually, classify 5 hand-picked messages — no sklearn
- [ ] Then the interview line is: "I can build Naive Bayes from first principles"

### ☐ 10. README Deprecation Fixes
- [ ] `Generative AI Projects/Krishi Mitra AI/README.md`: remove or fulfil the Dockerfile claim
- [ ] Re-verify every "Live Demo" badge — dead or placeholder links damage trust

### ☐ 11. Root README Accuracy Fix ⚠️ important
- [ ] Roadmap status table (line ~210): mark Months 1–3 honestly — e.g. `3 | Core Machine Learning | 🟡 concepts done, assigned projects in rework`
- [ ] Or finish the missing Month 1–3 projects and then mark honestly
- **Why:** Recruiters cross-check claims against pinned repos. Unverifiable = credibility risk.

### ☐ 12. ReAct Pattern + Agent Memory — Month 5, Week 3 (optional)
- [ ] One notebook: build a tiny ReAct loop (Thought → Action → Observation → Thought) by hand with tool calling
- [ ] Add LangGraph/checkpointer memory to one agent

---

## 📁 Bonus: Month 1-Level Micro-Projects (fill if time permits)

- [ ] Simple calculator (input → +/−/×/÷)
- [ ] Student grade calculator reading names+marks from `.txt`
- [ ] IPL analysis (top run-scorers, economy, win %) — replaces the Zomato/Covid EDA if pressed for time
- [ ] Stock analysis mini-notebook (daily returns mean, std = risk, correlation matrix on Nifty 50 stocks) — *this is also an interview favourite*
- These matter less than Tiers 1–2 — they're practice artifacts, not portfolio pieces.

---

## ✅ Not Needed — Already Done (do NOT redo)

- PyTorch manual training loops (loss.backward / optimizer.step) across ANN/CNN/RNN
- EfficientNet-B0 Indian Food classifier — exact roadmap match, live demo
- Transformers theory (attention, encoder/decoder, masks, cross-attention)
- Full RAG pipeline: loaders (PDF/web/Arxiv) → 3 splitters (char/token/semantic) → retrievers (MMR, multi-query) → Chroma/FAISS with page-level citations
- Tool-calling + multi-agent + LLM-router (Tavily, custom tools, Runnables)
- FastAPI fundamentals (5 lessons) + Pydantic (6 lessons)
- pytest + GitHub Actions CI (Aether)
- 9+ live Streamlit deployments
- 3 SQL projects (E-Commerce, Library, Students Management) — already ahead of the roadmap here
- Hinglish/multilingual chatbots: Multi Lingular (deployed) + BankSaathi

---

## 🧭 After Tiers 1–2 Are Done → Month 6 Start Plan (Day 1)

1. **Pick the 3 capstones** (depth > breadth):
   - Capstone A (GenAI): level up **Aether** — multi-agent + RAG + real FastAPI backend + tests
   - Capstone B (GenAI serving): the FastAPI RAG bot from item 5, Dockerized
   - Capstone C (Modeling): the fine-tuned BERT from item 4 with proper F1 metrics
2. **1-page resume:** 3 projects, each with name + 2-line description + one metric + link
3. **README "Featured Projects" table:** trim to the best 3–5, every link verified
4. **LinkedIn:** headline + About + 3 posts drafted ("I built X with Y, achieved Z")
5. Start applying from Week 2 of Month 6 — don't wait for "readiness."

---

*Tracker auto-generated from a repo audit. Update checkboxes as things land. A box is "done" only when the evidence file exists in this repo.*
