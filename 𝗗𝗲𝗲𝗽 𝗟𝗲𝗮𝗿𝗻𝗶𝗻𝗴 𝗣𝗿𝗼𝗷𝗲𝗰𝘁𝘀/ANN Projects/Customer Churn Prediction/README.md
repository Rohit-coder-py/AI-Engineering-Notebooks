# 📉 Customer Churn Prediction

An end-to-end deep learning project that predicts whether a telecom customer
is going to **churn** (cancel their subscription), using a PyTorch Artificial
Neural Network trained on the classic Telco Customer Churn dataset.

---

## Business Problem

Acquiring a new customer costs a lot more than keeping an existing one. This
project builds a model that flags customers who are likely to churn based on
their account details, contract type, and the services they've signed up
for — so retention teams can step in before the customer leaves.

**Task type:** Binary classification (`Churn`: 1 = churns, 0 = stays)

---

## Dataset

- **Source:** Telco Customer Churn dataset (`Telco-Customer-Churn.csv`)
- **Size:** ~7,032 rows (after dropping rows with missing `TotalCharges`), 19 features
- **Class balance:** roughly 73% stay vs 27% churn — imbalanced, handled with
  a `pos_weight` term in the loss function

**Features used:** gender, SeniorCitizen, Partner, Dependents, tenure,
PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup,
DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract,
PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges.

`customerID` was dropped — it's a pure identifier with no predictive value.

---

## EDA Highlights

- The dataset is imbalanced (~27% churn), so accuracy alone is a misleading
  metric — precision, recall, F1, and ROC-AUC are tracked too.
- `tenure` is the strongest signal: customers who churn tend to have been
  around for a much shorter time.
- `MonthlyCharges` skews higher for churners; `TotalCharges` skews lower
  (they leave before charges add up).
- `Month-to-month` contracts churn far more than one/two-year contracts —
  no lock-in makes it easy to leave.
- `Fiber optic` internet customers churn more than DSL customers.

See `images/` for the saved EDA charts (target distribution, numeric
distributions, correlation heatmap, categorical churn rates) and
`notebooks/Customer Churn Prediction.ipynb` for the full walkthrough.

---

## Model

A feed-forward ANN (PyTorch `nn.Module`) with:

- 3 hidden layers (64 → 32 → 16 units), ReLU activations
- Single logit output, `BCEWithLogitsLoss` with a `pos_weight` term to
  correct for class imbalance
- Adam optimizer, lr = 1e-3, batch size 64

### Results (held-out test set, 1,055 rows)

| Metric | Score |
|---|---|
| Accuracy | 70.3% |
| Precision | 45.7% |
| Recall | 62.5% |
| F1 Score | 52.8% |
| ROC-AUC | 0.747 |

These come from the reference training run shipped with this repo
(`models/metrics.json`) — re-run `python src/train.py` (or the notebook) to
reproduce or improve on them. Confusion matrix and ROC curve are saved in
`images/06_confusion_matrix.png` and `images/07_roc_curve.png`.

---

## Project Structure

```
Customer Churn Prediction/
│
├── data/
│   └── cleaned_and_scaled_dataset.csv   # encoded dataset (pre-scaling)
├── notebooks/
│   └── Customer Churn Prediction.ipynb  # full walkthrough: EDA -> encoding -> training -> saving
├── src/
│   ├── model.py                          # PyTorch ANN architecture
│   ├── preprocessing.py                  # turns one raw form input into a model-ready row
│   ├── train.py                          # full training pipeline (run this to retrain)
│   └── infer.py                          # loads saved artifacts + predict() used by the app
├── models/
│   ├── churn_model_weights.npz          # trained weights
│   ├── scaler.pkl                        # fitted StandardScaler
│   ├── feature_order.pkl                 # exact feature column order
│   └── metrics.json                      # test-set metrics
├── app/
│   └── app.py                            # Streamlit inference UI (light theme)
├── images/                               # saved EDA + evaluation plots
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Running It

**Retrain from scratch:**
```bash
cd "Customer Churn Prediction"
pip install -r requirements.txt
python src/train.py
```

**Launch the app:**
```bash
streamlit run app/app.py
```

The app ships with an already-trained model in `models/`, so it works right
away — retraining is optional.

**Deploy (Streamlit Community Cloud):** push this repo to GitHub and point
Streamlit Community Cloud at `app/app.py` as the entry file. The
`.streamlit/config.toml` in this repo pins a light theme so the app never
renders dark, regardless of the visitor's system settings.

---

## Future Improvements

- Try tree-based baselines (XGBoost/LightGBM) as a sanity-check comparison
  against the ANN
- Add SHAP-based feature importance / explainability to the app
- k-fold cross-validation instead of a single train/valid/test split, for a
  more robust performance estimate
- Tune the classification threshold instead of the default 0.5, since
  recall on churners matters more than raw accuracy here

---

## Disclaimer

This model is a **screening tool built for a data science portfolio**, not
a production-grade retention system. Predictions should be treated as a
starting point for a human decision, not a final verdict on any customer.
