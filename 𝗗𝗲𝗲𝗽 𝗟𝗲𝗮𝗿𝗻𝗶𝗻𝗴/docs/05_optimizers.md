# ⚙️ Optimizers — Complete Revision

> An **optimizer** decides *how* the model's weights are updated using the gradients computed during backpropagation.

---

## 1. Gradient Descent (Batch GD)
- **What:** Computes gradient using the **entire dataset** before one update.
- **Use when:** Very small datasets only.
- **⚠️ Watch out:** Extremely slow and memory-heavy on real datasets — rarely used in practice.

---

## 2. Stochastic Gradient Descent (SGD)
- **What:** Updates weights using **one sample at a time**.
- **Use when:** Rarely used alone today, but forms the base of all modern optimizers.
- **⚠️ Watch out:** Very noisy updates, unstable convergence.

---

## 3. Mini-Batch Gradient Descent (SGD with batches)
- **What:** Updates weights using small batches (e.g., 32, 64, 128 samples) — the real-world default.
- **Use when:** Standard for almost all deep learning training.
- **PyTorch:** `torch.optim.SGD(model.parameters(), lr=0.01)`

---

## 4. SGD with Momentum
- **What:** Adds a "velocity" term so updates keep moving in a consistent direction, smoothing out noisy gradients and speeding convergence.
- **Use when:** You want faster, more stable convergence than plain SGD; common in **CNN training** (e.g., ResNet was trained with SGD + momentum).
- **PyTorch:** `torch.optim.SGD(params, lr=0.01, momentum=0.9)`

---

## 5. Adagrad
- **What:** Adapts learning rate **per parameter** — larger updates for infrequent features, smaller for frequent ones.
- **Use when:** Sparse data (e.g., NLP with sparse word features).
- **⚠️ Watch out:** Learning rate shrinks too aggressively over time, can stop learning too early.

---

## 6. RMSProp
- **What:** Fixes Adagrad's shrinking learning rate problem using a moving average of squared gradients.
- **Use when:** **RNN/LSTM training** — historically a strong choice for sequential data.

---

## 7. Adam (Adaptive Moment Estimation)
- **What:** Combines **Momentum** (1st moment) + **RMSProp** (2nd moment) — adaptive learning rate per parameter with momentum.
- **Use when:** **The default choice for almost everything** in modern deep learning — fast convergence, works well out-of-the-box.
- **Professional use:** Most widely used optimizer in industry & research (default in most papers/tutorials).
- **PyTorch:** `torch.optim.Adam(model.parameters(), lr=0.001)`

---

## 8. AdamW
- **What:** Adam with **decoupled weight decay** (proper L2 regularization, fixes a subtle bug in original Adam's weight decay implementation).
- **Use when:** Training **Transformers** (BERT, GPT, ViT) — this is the standard optimizer for modern large models.
- **Professional use:** Default optimizer in almost all Hugging Face / LLM training scripts today.
- **PyTorch:** `torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.01)`

---

## 9. Nadam
- **What:** Adam + Nesterov momentum (looks ahead before updating).
- **Use when:** Occasionally used when you want the benefits of Adam with slightly better convergence behavior — less common in practice.

---

## 🎯 Quick Decision Table

| Situation | Best Optimizer |
|---|---|
| Default / not sure | **Adam** |
| Training Transformers/LLMs | **AdamW** |
| Training CNNs (image classification, e.g. ResNet) | **SGD + Momentum** (often better final accuracy than Adam) |
| Sparse data (NLP, embeddings) | Adagrad / Adam |
| RNN / LSTM | RMSProp / Adam |
| Need best generalization + willing to tune more | SGD + Momentum + LR scheduler |

> 💡 **Professional habit:** Start with **Adam (lr=1e-3)** to quickly get a working baseline. If chasing the *last bit* of accuracy for a CNN (e.g., for a paper or competition), switch to **SGD + Momentum** with a learning-rate scheduler — it often generalizes better, just needs more tuning and training time.

---

## Learning Rate — The Most Important Hyperparameter
- **Too high** → loss explodes / diverges / oscillates
- **Too low** → training is painfully slow, may get stuck in bad local minima
- **Professional tools:**
  - `torch.optim.lr_scheduler.StepLR` — decay LR every N epochs
  - `torch.optim.lr_scheduler.ReduceLROnPlateau` — decay when validation loss stalls
  - `torch.optim.lr_scheduler.CosineAnnealingLR` — smooth cosine decay (popular in modern training)
  - **Learning Rate Warmup** — start small, increase, then decay (standard for Transformers)
