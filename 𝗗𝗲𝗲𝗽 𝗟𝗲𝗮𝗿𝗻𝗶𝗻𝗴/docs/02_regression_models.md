# 📈 Regression Models — Complete Revision

> **Regression** predicts a **continuous numeric value** (price, temperature, salary, etc.)

---

## 1. Linear Regression
- **What:** Fits a straight line `y = wx + b` (or hyperplane for multiple features) minimizing error.
- **Use when:** Relationship between input and output is roughly linear; small/medium tabular data.
- **Loss used:** Mean Squared Error (MSE)
- **Professional use:** Baseline model for any regression task — always try this first before anything complex.

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X_train, y_train)
```

---

## 2. Polynomial Regression
- **What:** Extends linear regression by adding polynomial terms (x², x³...) to fit curved data.
- **Use when:** Data shows a **non-linear but smooth** trend.
- **⚠️ Watch out:** High-degree polynomials **overfit** easily — always cross-validate the degree.

---

## 3. Ridge Regression (L2 Regularization)
- **What:** Linear regression + **L2 penalty** (shrinks coefficients toward zero, never exactly zero).
- **Use when:** You have **multicollinearity** (features are correlated) or many features causing overfitting.
- **Professional tip:** Ridge is preferred when you believe *most* features are useful but need to control their magnitude.

---

## 4. Lasso Regression (L1 Regularization)
- **What:** Linear regression + **L1 penalty** (can shrink coefficients to exactly **zero** → automatic feature selection).
- **Use when:** You suspect only a **subset of features** actually matter (sparse solutions).
- **Professional tip:** Use Lasso when you want an interpretable model with fewer active features.

---

## 5. Elastic Net
- **What:** Combines L1 + L2 penalties (best of Ridge + Lasso).
- **Use when:** Many correlated features **and** you want feature selection — a balanced middle ground.

---

## 6. Decision Tree Regressor
- **What:** Splits data into regions using if-else rules, predicts average value per region.
- **Use when:** Data has non-linear relationships and you need interpretability.
- **⚠️ Watch out:** Prone to overfitting if depth isn't controlled (`max_depth`).

---

## 7. Random Forest Regressor
- **What:** An **ensemble** of many decision trees, averaging their predictions.
- **Use when:** You want strong performance on tabular data with minimal tuning.
- **Professional use:** One of the most common go-to models in industry for tabular regression — robust, hard to overfit.

---

## 8. Gradient Boosting (XGBoost / LightGBM / CatBoost)
- **What:** Builds trees **sequentially**, each new tree corrects errors of the previous ones.
- **Use when:** You need the **best possible accuracy** on structured/tabular data.
- **Professional use:** The default winner in Kaggle competitions and real-world tabular ML — XGBoost/LightGBM are industry standard.

---

## 9. Support Vector Regression (SVR)
- **What:** Fits a function within a margin of tolerance (epsilon-tube), robust to outliers.
- **Use when:** Small-to-medium datasets with complex but smooth relationships.
- **⚠️ Watch out:** Doesn't scale well to very large datasets.

---

## 10. Neural Network Regression (ANN)
- **What:** A feedforward neural net with a **single linear output neuron** (no activation on output layer).
- **Use when:** Very large datasets, complex non-linear relationships, or regression is part of a bigger deep learning pipeline.
- **Loss used:** MSE or MAE
- **PyTorch tip:** Last layer = `nn.Linear(hidden_dim, 1)` with **no activation function** (identity output).

---

## 🎯 Quick Decision Table

| Situation | Best Model |
|---|---|
| Simple, small, linear data | Linear Regression |
| Many correlated features | Ridge |
| Need automatic feature selection | Lasso |
| Best tabular accuracy | XGBoost / LightGBM |
| Need interpretability | Decision Tree / Linear Regression |
| Huge dataset, complex patterns | Neural Network (ANN) |
| Robust to outliers, small data | SVR |

> 💡 **Professional habit:** Always start with Linear Regression as a baseline. If R² is poor, move to tree-based ensembles (Random Forest/XGBoost) before jumping to deep learning — DL regression is rarely needed unless data is huge or part of a larger pipeline (e.g., regression head on top of a CNN).
