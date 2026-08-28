# 🎯 Classification Models — Complete Revision

> **Classification** predicts a **discrete category/label** (spam/not spam, cat/dog, disease type).

---

## 1. Logistic Regression
- **What:** Despite the name, it's a **classifier**. Uses the sigmoid function to output a probability (0–1).
- **Use when:** Binary classification, need interpretability, linearly separable-ish data.
- **Loss used:** Binary Cross-Entropy
- **Professional use:** The go-to **baseline** for any classification task (like Linear Regression for regression).

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression().fit(X_train, y_train)
```

---

## 2. K-Nearest Neighbors (KNN)
- **What:** Classifies a point based on the majority label of its `k` nearest neighbors.
- **Use when:** Small dataset, no assumptions about data distribution needed.
- **⚠️ Watch out:** Slow at prediction time on large datasets (must compute distance to all points); sensitive to feature scaling.

---

## 3. Support Vector Machine (SVM)
- **What:** Finds the **optimal hyperplane** that maximizes the margin between classes. Kernel trick (RBF, polynomial) handles non-linear boundaries.
- **Use when:** Medium-sized datasets, clear margin of separation, high-dimensional data (e.g., text classification).
- **Professional use:** Very strong on small-to-medium, high-dimensional data like text (before deep learning took over NLP).

---

## 4. Naive Bayes
- **What:** Probabilistic classifier based on Bayes' theorem, assumes feature independence ("naive").
- **Use when:** Text classification (spam filtering, sentiment), very fast, works well with small data.
- **Professional use:** Extremely popular for **spam detection** and simple NLP baselines.

---

## 5. Decision Tree Classifier
- **What:** Splits data using if-else rules based on feature thresholds.
- **Use when:** Need a highly interpretable model (e.g., explain to non-technical stakeholders).
- **⚠️ Watch out:** Overfits easily — always tune `max_depth`, `min_samples_split`.

---

## 6. Random Forest Classifier
- **What:** Ensemble of decision trees using majority voting.
- **Use when:** Strong, reliable performance on tabular data with minimal tuning needed.
- **Professional use:** Extremely common default choice in industry for structured data classification.

---

## 7. Gradient Boosting (XGBoost / LightGBM / CatBoost)
- **What:** Sequential ensemble, each tree fixes previous errors.
- **Use when:** You need top-tier accuracy on structured/tabular classification.
- **Professional use:** Dominates Kaggle & real-world tabular classification tasks (credit scoring, churn prediction, fraud detection).

---

## 8. Neural Network Classifier (ANN)
- **What:** Feedforward network with:
  - **Binary classification:** 1 output neuron + **Sigmoid** activation
  - **Multi-class classification:** N output neurons + **Softmax** activation
- **Use when:** Large datasets, unstructured data (image/text/audio), or complex non-linear decision boundaries.
- **Loss used:** Binary Cross-Entropy (binary) / Categorical Cross-Entropy (multi-class)

```python
# PyTorch multi-class classifier head
self.output = nn.Linear(hidden_dim, num_classes)
# NOTE: don't apply Softmax manually if using nn.CrossEntropyLoss —
# it applies LogSoftmax internally!
```

---

## 9. CNN (for image classification)
- **What:** Uses convolutional layers to extract spatial features before classifying.
- **Use when:** Any image classification task.
- **Professional use:** Standard architecture for computer vision (ResNet, EfficientNet, etc. are all CNN variants).

---

## 10. Transformer-based Classifiers (BERT, etc.)
- **What:** Pretrained transformer + classification head fine-tuned on your data.
- **Use when:** Text classification tasks with enough compute — current state of the art for NLP.

---

## 🎯 Quick Decision Table

| Situation | Best Model |
|---|---|
| Simple binary baseline | Logistic Regression |
| Small dataset, no assumptions | KNN |
| Text classification (fast/simple) | Naive Bayes |
| High-dim data, clear margin | SVM |
| Best tabular accuracy | XGBoost / LightGBM |
| Need interpretability | Decision Tree |
| Images | CNN |
| Text (SOTA) | Transformer (BERT/RoBERTa) |
| Huge structured data, complex patterns | ANN |

> 💡 **Professional habit:** For **any** classification problem, check **class imbalance** first (`value_counts()`). If imbalanced, use `class_weight='balanced'`, **stratified** train/test split, and metrics like **F1-score / ROC-AUC** instead of plain accuracy.
