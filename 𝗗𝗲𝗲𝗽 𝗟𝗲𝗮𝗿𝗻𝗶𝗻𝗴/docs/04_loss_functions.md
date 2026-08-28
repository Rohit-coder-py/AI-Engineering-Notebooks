# 📉 Loss Functions — Complete Revision

> A **loss function** measures how wrong the model's prediction is. Training = minimizing this loss.

---

## 🔵 Regression Losses

### 1. Mean Squared Error (MSE / L2 Loss)
- **Formula:** `MSE = (1/n) Σ(y_true - y_pred)²`
- **Use when:** Default choice for regression; penalizes **large errors heavily** (squared term).
- **⚠️ Watch out:** Very sensitive to outliers (a single big error dominates the loss).
- **PyTorch:** `nn.MSELoss()`

### 2. Mean Absolute Error (MAE / L1 Loss)
- **Formula:** `MAE = (1/n) Σ|y_true - y_pred|`
- **Use when:** Dataset has **outliers** you don't want to over-penalize.
- **⚠️ Watch out:** Gradient is constant (not smooth at 0), can slow convergence.
- **PyTorch:** `nn.L1Loss()`

### 3. Huber Loss (Smooth L1)
- **What:** Combines MSE (small errors) + MAE (large errors) — best of both worlds.
- **Use when:** You want robustness to outliers **but** smooth gradients near zero.
- **Professional use:** Common in robust regression and object detection (bounding box regression).
- **PyTorch:** `nn.SmoothL1Loss()` / `nn.HuberLoss()`

---

## 🟢 Classification Losses

### 4. Binary Cross-Entropy (BCE / Log Loss)
- **Use when:** Binary classification (2 classes).
- **Pairs with:** Sigmoid activation on the output layer.
- **PyTorch:** `nn.BCELoss()` (needs manual sigmoid) or `nn.BCEWithLogitsLoss()` (**preferred** — combines sigmoid + BCE, more numerically stable).

### 5. Categorical Cross-Entropy
- **Use when:** Multi-class classification (labels are **one-hot encoded**).
- **Pairs with:** Softmax activation.

### 6. Cross-Entropy Loss (Sparse)
- **Use when:** Multi-class classification with **integer labels** (not one-hot) — the standard in PyTorch.
- **PyTorch:** `nn.CrossEntropyLoss()` — ⚠️ **combines LogSoftmax + NLLLoss internally**, so **never** add a Softmax layer before it!

```python
criterion = nn.CrossEntropyLoss()
loss = criterion(model_outputs_raw_logits, integer_labels)
```

### 7. Hinge Loss
- **Use when:** Training Support Vector Machines (SVM); margin-based classification.

### 8. Focal Loss
- **What:** Modified Cross-Entropy that **down-weights easy examples**, focuses on hard/misclassified ones.
- **Use when:** **Severe class imbalance** (e.g., object detection with many background vs few object pixels).
- **Professional use:** Standard in object detection models (RetinaNet).

---

## 🟣 Other Important Losses

### 9. KL Divergence (Kullback-Leibler)
- **Use when:** Measuring difference between two probability distributions — used in VAEs, knowledge distillation.

### 10. Contrastive Loss / Triplet Loss
- **Use when:** Similarity learning tasks — face recognition, embeddings (pull similar items close, push dissimilar apart).

### 11. Dice Loss / IoU Loss
- **Use when:** Image segmentation tasks — measures overlap between predicted and true masks.

---

## 🎯 Quick Decision Table

| Task | Loss Function |
|---|---|
| Regression (general) | MSE |
| Regression + outliers | MAE or Huber |
| Binary classification | BCEWithLogitsLoss |
| Multi-class classification | CrossEntropyLoss |
| Imbalanced classification | Focal Loss |
| SVM | Hinge Loss |
| Segmentation | Dice / IoU Loss |
| Embeddings / similarity | Triplet / Contrastive Loss |
| Generative models (VAE) | KL Divergence + Reconstruction Loss |

> 💡 **Professional habit:** In PyTorch, **always feed raw logits** (no Sigmoid/Softmax applied manually) into `BCEWithLogitsLoss` and `CrossEntropyLoss` — these combine the activation + loss internally for numerical stability. Applying Softmax/Sigmoid yourself first is one of the most common beginner bugs.
