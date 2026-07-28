# 🛡️ Fraud Sentinel — Credit Card Fraud Detection

A PyTorch neural network that screens credit-card transactions for fraud, with
a dark, professional Streamlit app for scoring transactions.

## Run it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy it (Streamlit Community Cloud)

1. Push this whole folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Point it at your repo, branch, and set the main file to `app.py`
4. Deploy — that's it, `requirements.txt` and `.streamlit/config.toml` are already set up

## What's inside

```
app.py                 ← the whole app (UI + model + prediction logic, one file)
requirements.txt       ← dependencies
.streamlit/config.toml ← dark theme
data/                  ← cleaned dataset
models/                ← trained model + preprocessing artifacts
images/                ← EDA & evaluation charts (used by the Analytics/Performance pages)
notebooks/              ← the full training notebook (EDA + training + evaluation)
```

## Results (held-out test set, 50,942 transactions)

| Metric | Legitimate | Fraud |
|---|---|---|
| Precision | 99.65% | 73.33% |
| Recall | 99.94% | 32.84% |

**Accuracy: 99.58%** · **ROC-AUC: 0.907**

Fraud is only 0.52% of transactions, so accuracy alone is misleading — see the
**Model Performance** page in the app for the honest read.

## Disclaimer

Portfolio project — not a certified fraud-detection system.
