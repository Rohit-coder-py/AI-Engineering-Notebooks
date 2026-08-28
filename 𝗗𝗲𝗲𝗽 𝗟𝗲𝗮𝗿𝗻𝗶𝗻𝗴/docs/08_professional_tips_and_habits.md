# 🌟 Professional Tips & Habits for an AI/ML Engineer

> These are the habits that separate a student who "makes models" from an engineer who **ships reliable ones**. Read this file periodically, not just once.

---

## 1. Always Build a Baseline First
Never jump straight to a complex model. Start with:
- **Regression** → Linear Regression
- **Classification** → Logistic Regression
- **Deep tasks** → A small ANN

> If your fancy model doesn't beat the simple baseline by a meaningful margin, the fancy model isn't worth the complexity.

---

## 2. Understand Your Data Before Touching a Model
- Check for **missing values**, **class imbalance**, **outliers**, **data leakage**.
- Plot distributions (histograms, boxplots) before modeling — a 5-minute EDA saves hours of debugging later.

---

## 3. Never Trust a Single Metric
- Accuracy alone is **misleading on imbalanced data**. Use Precision, Recall, F1-score, ROC-AUC, Confusion Matrix.
- For regression: check R², MAE, and **residual plots** — not just MSE.

---

## 4. Always Split Data Properly
- **Train / Validation / Test** — never evaluate on data the model has seen.
- Use **stratified splits** for classification with imbalance.
- For time-series: split **chronologically**, never randomly (avoid data leakage from the future).

---

## 5. Version Everything
- Use **Git** for code (you're already doing this with your GitHub portfolio — keep it up!).
- Track experiments: hyperparameters, metrics, model versions. Tools: **Weights & Biases (wandb)**, **MLflow**, or even a simple spreadsheet when starting out.

---

## 6. Reproducibility Matters
```python
import torch, numpy as np, random
seed = 42
torch.manual_seed(seed)
np.random.seed(seed)
random.seed(seed)
```
> Professionals always **set seeds** so results can be reproduced and debugged reliably.

---

## 7. Read the Official Docs, Not Just Tutorials
- PyTorch docs (`pytorch.org/docs`) are excellent and precise — tutorials often skip edge cases.
- When stuck, search the **exact error message** — someone has almost certainly hit it before (GitHub issues, StackOverflow).

---

## 8. Comment Your "Why", Not Your "What"
```python
# Bad comment:
# add dropout
x = self.dropout(x)

# Good comment:
# Dropout(0.3) added here after observing overfitting (train acc 98%, val acc 74%)
x = self.dropout(x)
```

---

## 9. Keep a "Model Card" / Experiment Log
For every serious model you train, note down:
- Architecture used
- Hyperparameters (lr, batch size, epochs)
- Final train/val metrics
- What worked, what didn't

> This is exactly what top ML teams (and your own GitHub `My_Projects` repo) should reflect — it shows recruiters you think like an engineer, not just a student running notebooks.

---

## 10. Learn to Read Loss Curves
- **Train loss ↓, Val loss ↓** → good, keep training.
- **Train loss ↓, Val loss ↑** → **overfitting** — add regularization, reduce model size, or get more data.
- **Both flat/high** → **underfitting** — increase model capacity, train longer, or check learning rate.

---

## 11. Don't Fear Rewriting Code
Your first working version is rarely your best version. Professionals refactor:
messy notebook → clean functions → reusable modules/classes.

---

## 12. Build Projects End-to-End
Don't stop at "I trained a model in a notebook." Practice:
- Saving/loading models (`torch.save` / `torch.load`)
- Wrapping in a simple API (FastAPI/Flask)
- Basic deployment (Streamlit demo, Hugging Face Spaces)

> This full-cycle thinking is exactly what makes a portfolio project stand out for **internship applications**.

---

## 13. Stay Curious, Read Papers (Slowly)
- Don't wait until you "understand everything" to start reading papers — read abstracts + conclusions first, build up.
- Great starting points: "Attention is All You Need," "Deep Residual Learning" (ResNet), "Adam: A Method for Stochastic Optimization."

---

## 14. Explain Your Work Out Loud
If you can't explain **why** you chose Adam over SGD, or ReLU over Sigmoid, to a friend in simple words — you don't fully understand it yet. This is the best self-test before an interview.

---

## 15. Compute Isn't Everything — Thinking Is
Many beginners think "bigger model = better." In reality, most real-world wins come from:
- Better data cleaning
- Better feature engineering
- Correct evaluation metrics
- Careful debugging

> A well-tuned Logistic Regression often beats a poorly-built neural network. **Think before you build.**

---

### 🎯 One-Line Summary
> **Baseline → Understand data → Experiment carefully → Track everything → Explain clearly → Iterate.**
