# ⚡ Activation Functions — Complete Revision

> Activation functions introduce **non-linearity** into a network. Without them, a neural network — no matter how many layers — would collapse into a single linear function.

---

## 1. Sigmoid
- **Formula:** `σ(x) = 1 / (1 + e^-x)` → output range **(0, 1)**
- **Use when:** Output layer of **binary classification** (interpreted as probability).
- **⚠️ Watch out:** **Vanishing gradient** problem in deep networks — gradients shrink to near-zero for large |x|. Avoid using in hidden layers of deep nets.

---

## 2. Tanh (Hyperbolic Tangent)
- **Formula:** output range **(-1, 1)**, zero-centered
- **Use when:** Hidden layers of shallow networks, RNNs (historically common in LSTM gates).
- **⚠️ Watch out:** Still suffers from vanishing gradients, just less severe than sigmoid (zero-centered helps).

---

## 3. ReLU (Rectified Linear Unit)
- **Formula:** `f(x) = max(0, x)`
- **Use when:** **Default choice for hidden layers** in almost all modern deep networks (CNNs, ANNs).
- **Why it's popular:** Computationally cheap, doesn't saturate for positive values, avoids vanishing gradient for x > 0.
- **⚠️ Watch out:** **"Dying ReLU" problem** — neurons can get stuck outputting 0 forever if they enter the negative region.
- **PyTorch:** `nn.ReLU()`

---

## 4. Leaky ReLU
- **Formula:** `f(x) = x if x>0 else αx` (small slope α, e.g., 0.01, for negative values)
- **Use when:** You're seeing dying ReLU issues — allows a small gradient to flow even for negative inputs.
- **PyTorch:** `nn.LeakyReLU(negative_slope=0.01)`

---

## 5. Parametric ReLU (PReLU)
- **What:** Like Leaky ReLU, but `α` is a **learnable parameter** instead of fixed.
- **Use when:** Large datasets where you want the network to learn the optimal negative slope itself.

---

## 6. ELU (Exponential Linear Unit)
- **What:** Smooths out the negative region using an exponential curve instead of a straight line.
- **Use when:** You want faster convergence and outputs closer to zero-mean than ReLU.
- **⚠️ Watch out:** More computationally expensive (uses `exp()`).

---

## 7. Softmax
- **What:** Converts a vector of raw scores (logits) into a **probability distribution** that sums to 1.
- **Use when:** **Output layer** of **multi-class classification** (one probability per class).
- **⚠️ PyTorch tip:** If using `nn.CrossEntropyLoss`, do **NOT** apply Softmax manually — it's built into the loss function already.

---

## 8. GELU (Gaussian Error Linear Unit)
- **What:** A smooth, probabilistic version of ReLU.
- **Use when:** **Transformers** (BERT, GPT, ViT) — this is the standard activation in modern NLP/vision transformer architectures.
- **PyTorch:** `nn.GELU()`

---

## 9. Swish / SiLU
- **Formula:** `f(x) = x · sigmoid(x)`
- **Use when:** Used in some modern CNN architectures (EfficientNet) — often slightly outperforms ReLU on deep models.
- **PyTorch:** `nn.SiLU()`

---

## 🎯 Quick Decision Table

| Where | Best Activation |
|---|---|
| Hidden layers (general/default) | **ReLU** |
| Hidden layers, dying ReLU issue | Leaky ReLU / PReLU / ELU |
| Output — Binary classification | Sigmoid |
| Output — Multi-class classification | Softmax |
| Output — Regression | **None** (Linear/Identity) |
| Transformers (BERT/GPT/ViT) | GELU |
| Modern CNNs (EfficientNet-style) | Swish/SiLU |
| RNN/LSTM gates | Sigmoid + Tanh (standard LSTM design) |

---

## 🧠 Visual Intuition (Text Form)

```
Sigmoid:  ______/‾‾‾‾‾‾   (squashes to 0–1, saturates both ends)
Tanh:     ‾‾\____/‾‾‾‾    (squashes to -1–1, zero-centered)
ReLU:     ____/‾‾‾‾‾‾‾    (0 for negative, linear for positive)
LeakyReLU:‾‾\_/‾‾‾‾‾‾‾    (small negative slope instead of flat 0)
```

> 💡 **Professional habit:** Default to **ReLU** for hidden layers unless you're building a Transformer (use **GELU**) or seeing dying neurons (try **Leaky ReLU**). Never use Sigmoid/Tanh in deep hidden layers — reserve them for output layers or gates in RNNs/LSTMs.
