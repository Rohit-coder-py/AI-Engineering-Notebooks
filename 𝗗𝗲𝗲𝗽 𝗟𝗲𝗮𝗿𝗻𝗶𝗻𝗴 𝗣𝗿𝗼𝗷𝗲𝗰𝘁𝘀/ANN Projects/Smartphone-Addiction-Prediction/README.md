# 📱 Smartphone Usage & Addiction Prediction

An end-to-end deep learning project that predicts whether a person's
smartphone usage pattern qualifies as **addictive**, using a PyTorch
Artificial Neural Network trained on behavioural and demographic data.

---

## Business Problem

Excessive smartphone use is linked to disrupted sleep, lower academic/work
performance, and elevated stress. This project builds a screening model
that flags addictive usage risk from simple, self-reportable inputs —
screen time, social media hours, sleep, notification volume, stress level,
and a few demographics — so the risk can be surfaced early, before it's a
crisis.

**Task type:** Binary classification (`addicted_label`: 1 = addictive
pattern, 0 = not)

---

## Dataset

- **Source:** [Kaggle — Smartphone Usage And Addiction Analysis](https://www.kaggle.com/datasets/jayjoshi37/smartphone-usage-and-addiction-prediction)
- **Size:** 7,500 rows, 16 columns
- **Class balance:** 5,308 addicted (70.8%) vs 2,192 not addicted (29.2%)

**Features used:**

| Feature | Type | Description |
|---|---|---|
| age | numeric | 18–35 |
| daily_screen_time_hours | numeric | Total daily screen time |
| social_media_hours | numeric | Daily social media use |
| gaming_hours | numeric | Daily gaming use |
| work_study_hours | numeric | Daily work/study screen use |
| sleep_hours | numeric | Daily sleep |
| notifications_per_day | numeric | Notification count |
| app_opens_per_day | numeric | App-open count |
| weekend_screen_time | numeric | Weekend screen time |
| gender | categorical | Male / Female / Other |
| stress_level | categorical | Low / Medium / High |
| academic_work_impact | categorical | Self-reported Yes/No |

**Important — data leakage found and removed:** the raw dataset includes an
`addiction_level` column (Mild / Moderate / Severe) that maps **perfectly**
onto the target (`Mild → 0`, `Moderate`/`Severe → 1`). Since it's derived
directly from the label, it was dropped before modelling — along with
`transaction_id` and `user_id`, which are pure identifiers.

---

## EDA Highlights

- `social_media_hours` and `daily_screen_time_hours` show the strongest
  positive relationship with addiction risk.
- `sleep_hours` is negatively correlated — more sleep, lower risk.
- `stress_level = High` and `academic_work_impact = Yes` skew heavily
  toward the addicted class.
- `gender` is only a weak standalone predictor.

See `images/` for the full set of EDA charts (target distribution, feature
histograms, correlation heatmap, categorical breakdowns) and
`notebooks/Main.ipynb` for the full walkthrough with narrative.

---

## Model

A feed-forward ANN (PyTorch `nn.Module`) with:

- 3 hidden layers (64 → 32 → 16 units), ReLU activations, dropout (0.2)
- Single logit output, `BCEWithLogitsLoss` with a `pos_weight` term to
  correct for class imbalance
- Adam optimizer, lr = 5e-4, batch size 32, 60 epochs

Three hyperparameter configurations (baseline / deeper / wide-lowlr) were
trained and compared on validation F1; the `wide_lowlr` config won and was
used for the final saved model.

### Results (held-out test set, 1,125 rows)

| Metric | Score |
|---|---|
| Accuracy | 93.9% |
| Precision | 99.2% |
| Recall | 92.1% |
| F1 Score | 95.5% |
| ROC-AUC | 0.989 |

Confusion matrix and ROC curve are saved in `images/06_confusion_matrix.png`
and `images/07_roc_curve.png`.

---

## Project Structure

```
Smartphone-Addiction-Prediction/
│
├── data/
│   └── Smartphone_Usage_And_Addiction_Analysis_7500_Rows.csv
├── notebooks/
│   └── Main.ipynb            # Full narrative walkthrough, phases 1-19
├── src/
│   ├── preprocessing.py      # Cleaning, encoding, scaling
│   ├── model.py               # PyTorch ANN architecture
│   ├── train.py                # Full training pipeline (run this to retrain)
│   └── infer.py                 # Load model + predict() used by the app
├── models/
│   ├── addiction_model.pth   # Trained weights
│   ├── scaler.pkl             # Fitted StandardScaler
│   ├── encoders.pkl           # One-hot column mapping
│   ├── feature_order.pkl     # Exact feature column order
│   └── metrics.json           # Final test-set metrics
├── app/
│   └── app.py                  # Streamlit inference UI
├── images/                     # Saved EDA + evaluation plots
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Running It

**Retrain from scratch:**
```bash
cd Smartphone-Addiction-Prediction
pip install -r requirements.txt
python src/train.py
```

**Launch the app:**
```bash
streamlit run app/app.py
```

**Deploy:** push this repo to GitHub and point Streamlit Community Cloud
at `app/app.py` as the entry file.

---

## Future Improvements

- Try tree-based baselines (XGBoost/LightGBM) as a sanity-check comparison
  against the ANN
- Add SHAP-based feature importance / explainability to the app
- Collect more granular time-of-day usage data instead of daily totals
- k-fold cross-validation instead of a single train/val/test split, for a
  more robust performance estimate

---

## Disclaimer

This model is a **screening tool built for a data science portfolio**, not
a clinical or diagnostic instrument. Predictions should not be used to make
real decisions about anyone's mental health or wellbeing.
