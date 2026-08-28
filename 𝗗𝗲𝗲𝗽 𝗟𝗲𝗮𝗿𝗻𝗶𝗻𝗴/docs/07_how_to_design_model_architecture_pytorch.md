# 🏗️ How to Design a Model Architecture (PyTorch Guide)

> A step-by-step professional framework for deciding **what architecture to build**, then **how to actually build it in PyTorch**.

---

## Step 1: Understand the Problem Type First

| Data Type | Go-to Architecture |
|---|---|
| Tabular / structured | ANN (MLP) or Gradient Boosting (XGBoost) |
| Images | CNN (ResNet, EfficientNet) |
| Sequential / Time-series | RNN/LSTM/GRU or Transformer |
| Text/NLP | Transformer (BERT-style) |
| Generative tasks | GAN / VAE / Diffusion |
| Graph data | GNN |

> 📌 **Rule #1:** The data type decides the architecture family. Don't force a CNN on tabular data or an ANN on images.

---

## Step 2: Decide Depth & Width (for ANN/MLP)

- **Start small.** Begin with 1–2 hidden layers. Add depth only if the model **underfits**.
- **Width (neurons per layer):** A common professional pattern is a **funnel shape** — start wide, narrow down toward the output.
  ```
  Input (e.g. 20 features) → 128 → 64 → 32 → Output
  ```
- **Rule of thumb:** More layers = more capacity to learn complex patterns, but also more risk of overfitting and vanishing gradients. Don't go deep just because you can.

---

## Step 3: Choose Activations (see `06_activation_functions.md`)
- Hidden layers → **ReLU** (default)
- Output layer → depends on task (Sigmoid / Softmax / None)

---

## Step 4: Add Regularization (Prevent Overfitting)

| Technique | What it does | PyTorch |
|---|---|---|
| **Dropout** | Randomly zeroes neurons during training, forces redundancy | `nn.Dropout(p=0.3)` |
| **Batch Normalization** | Normalizes layer inputs, stabilizes & speeds up training | `nn.BatchNorm1d(num_features)` |
| **Weight Decay (L2)** | Penalizes large weights | set in optimizer: `weight_decay=1e-4` |
| **Early Stopping** | Stop training when validation loss stops improving | manual loop or a library callback |

> 💡 **Professional pattern:** `Linear → BatchNorm → ReLU → Dropout` is a very common and effective block ordering.

---

## Step 5: Build the Model in PyTorch

```python
import torch
import torch.nn as nn

class MyANN(nn.Module):
    def __init__(self, input_dim, num_classes):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(64, num_classes)   # raw logits — no Softmax here!
        )

    def forward(self, x):
        return self.net(x)
```

---

## Step 6: Choose Loss + Optimizer (see other files)

```python
model = MyANN(input_dim=20, num_classes=3)
criterion = nn.CrossEntropyLoss()                    # multi-class
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
```

---

## Step 7: The Standard PyTorch Training Loop (Memorize This Pattern)

```python
for epoch in range(num_epochs):
    model.train()
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()          # 1. clear old gradients
        outputs = model(X_batch)       # 2. forward pass
        loss = criterion(outputs, y_batch)  # 3. compute loss
        loss.backward()                # 4. backpropagation
        optimizer.step()               # 5. update weights

    # ---- Validation ----
    model.eval()
    with torch.no_grad():
        val_loss = 0
        for X_val, y_val in val_loader:
            val_outputs = model(X_val)
            val_loss += criterion(val_outputs, y_val).item()
    print(f"Epoch {epoch+1}: val_loss = {val_loss/len(val_loader):.4f}")
```

> ⚠️ **Never skip `model.eval()` + `torch.no_grad()` during validation** — forgetting this is one of the most common PyTorch bugs (wastes memory, and BatchNorm/Dropout behave incorrectly).

---

## Step 8: Debugging Checklist (Professional Habit)

1. **Overfit on a tiny batch first** (e.g., 10 samples) — if the model can't reach ~0 loss on 10 samples, there's a bug, not a data problem.
2. **Check loss goes down** in the first few epochs — if it's flat or NaN, check learning rate (too high → NaN, too low → flat).
3. **Check input normalization** — unnormalized features are a top cause of slow/unstable training.
4. **Check label encoding matches loss function** (e.g., `CrossEntropyLoss` wants integer class indices, NOT one-hot vectors).
5. **Print shapes** at every layer if something breaks — `print(x.shape)` inside `forward()` temporarily.

---

## Step 9: Architecture Design Checklist Before You Train

- [ ] Is my input data normalized/scaled?
- [ ] Does my output layer match my task (no activation for regression, Sigmoid for binary, raw logits for CrossEntropyLoss)?
- [ ] Do I have regularization (Dropout/BatchNorm) if the model is deep or data is small?
- [ ] Is my loss function correctly paired with my output layer?
- [ ] Have I split data into train/val/test (or used k-fold cross-validation)?
- [ ] Am I tracking both training and validation loss (to catch overfitting)?

---

## 🎯 General Architecture Design Philosophy

> **Start simple → get a working baseline → add complexity only when justified by validation metrics.**

This is the same principle across all of ML/DL:
1. Simple baseline (Logistic/Linear Regression)
2. Small ANN
3. Add regularization if overfitting
4. Add depth/width if underfitting
5. Switch to a specialized architecture (CNN/Transformer) only if the data type demands it
