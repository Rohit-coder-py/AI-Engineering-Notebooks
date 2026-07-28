# 🛡️ Fraud Sentinel — Credit Card Fraud Detection

A PyTorch neural network that screens credit-card transactions for fraud, wrapped
in a dark, premium Streamlit app for interactive scoring, batch upload, and
model-performance exploration.

## Dataset

339,607 real credit-card transactions across 14 merchant categories and 13
US states, with a **0.52% fraud rate** (1,782 fraud cases — a ~189:1
class imbalance). Source: [Kaggle — Credit Card Fraud
Dataset](https://www.kaggle.com/datasets/dhruvb2028/credit-card-fraud-dataset).

Features used (11 total): `merchant, category, amt, city, state, lat, long,
city_pop, job, merch_lat, merch_long`. Identifier/leakage columns
(`trans_date_trans_time`, `dob`, `trans_num`) are dropped before modelling.

## Model

A compact feed-forward network built in PyTorch:

```
Input (11) → Linear(16) → ReLU → Linear(8) → ReLU → Linear(1) → sigmoid
```

Trained with `BCEWithLogitsLoss` and Adam (lr=1e-3) for 10 epochs on a
70/15/15 train/validation/test split.

## Results (held-out test set, 50,942 transactions)

| Metric | Legitimate | Fraud |
|---|---|---|
| Precision | 99.65% | 73.33% |
| Recall | 99.94% | 32.84% |
| F1-score | 99.79% | 45.36% |

**Accuracy: 99.58%** &nbsp;·&nbsp; **ROC-AUC: 0.907**

Accuracy alone is misleading on this dataset — a model predicting "legitimate"
for everything would already score ~99.5%. The model's ROC-AUC of 0.91 shows it
has genuinely learned to rank risk well, but at the default 0.5 threshold it
only catches about 1 in 3 fraud cases (no class weighting was used, on purpose,
to keep the notebook's original training run intact — see the notebook's
"Conclusion & Next Steps" section for how to improve this).

## Project structure

```
Credit Card Fraud Detection/
├── app/                     # Streamlit app
│   ├── app.py                # main entry point / page router
│   ├── components.py         # reusable HTML/CSS UI components
│   ├── style.py               # theme CSS
│   └── data_utils.py         # cached data/model loaders
├── src/                     # reusable pipeline code
│   ├── model.py               # PyTorch model architecture
│   ├── preprocessing.py      # encoder/scaler wrapper
│   ├── infer.py               # inference helper used by the app
│   └── train.py               # standalone retraining script
├── notebooks/
│   └── Credit Card Fraud Detection.ipynb   # full EDA + training + evaluation
├── data/
│   ├── credit_card_frauds_cleaned.csv
│   └── data.md                # link to the raw Kaggle dataset
├── images/                  # saved EDA & evaluation plots
├── models/                  # trained weights + preprocessing artifacts
├── .streamlit/config.toml   # app theme
└── requirements.txt
```

## Running the app

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

The app has five pages:
- **Overview** — headline stats and a live transaction ticker
- **Predict** — score a single transaction (with real-sample autofill) or a
  batch CSV upload, with an adjustable decision threshold
- **Analytics** — the notebook's EDA charts with commentary
- **Model Performance** — confusion matrix, ROC curve, and an honest read of
  what the metrics mean given the class imbalance
- **About** — architecture, features, and tech stack

## Retraining

```bash
python src/train.py --data data/credit_card_frauds_cleaned.csv --models models
```

## Disclaimer

This is a data-science portfolio project, not a certified fraud-detection
system. Don't use it to make real financial or legal decisions.
