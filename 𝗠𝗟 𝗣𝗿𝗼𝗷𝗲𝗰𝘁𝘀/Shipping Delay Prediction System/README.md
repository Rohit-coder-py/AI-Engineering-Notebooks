# 📦 ShipSense — Shipment Delay Intelligence

A production-quality Streamlit application that predicts whether a shipment
will arrive **on time** or be **delayed**, before it leaves the warehouse —
built on a Stacking Classifier trained across 10 candidate models.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Model](https://img.shields.io/badge/Model-Stacking%20Classifier-6C63FF)
![F1](https://img.shields.io/badge/F1%20Score-0.7157-33D17A)

---

## ✨ Features

- **Live prediction** — enter shipment details and get an instant delay
  risk score with a confidence gauge
- **Explainable** — feature importance view showing which signals drive
  predictions
- **Analytics dashboard** — interactive delay-rate breakdowns by warehouse,
  shipment mode, product importance, weight, and discount
- **Full project narrative** — business problem, dataset, modeling, workflow
  and conclusion pages
- **Premium dark UI** — glassmorphism cards, animated route motif, metric
  cards, gauges, and smooth hover transitions
- **Defensive by design** — missing data/model files degrade gracefully
  with clear on-screen guidance instead of crashing

---

## 🗂️ Project Structure

```
.
├── app.py                     # Streamlit entry point (all pages/sections)
├── utils.py                   # Data & model loading, inference pipeline
├── styles.py                  # Design system: CSS tokens + components
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml            # Dark theme configuration
├── data/
│   ├── README.md
│   └── (cleaned.csv, raw_data.csv, ...)      # add your dataset(s)
├── models/
│   ├── README.md
│   └── (shipping_delay_model.pkl, scaler.pkl, *_encoder.pkl)  # add artifacts
├── graphs/
│   ├── README.md
│   └── (*.png)                # optional pre-rendered notebook graphs
└── notebook/
    └── shipping_delay_prediction_notebook.ipynb
```

## 🧩 Feature Set Used by the Model

| Feature | Type | Notes |
|---|---|---|
| `Warehouse_block` | Categorical | A, B, C, D, F |
| `Mode_of_Shipment` | Categorical | Flight, Road, Ship |
| `Customer_care_calls` | Numeric | Support calls for the order |
| `Cost_of_the_Product` | Numeric | Product cost |
| `Prior_purchases` | Numeric | Customer purchase history |
| `Product_importance` | Categorical | low, medium, high |
| `Discount_offered` | Numeric | Discount % |
| `Weight_in_gms` | Numeric | Package weight |

`ID`, `Gender`, and `Customer_rating` were dropped during feature engineering
(`Customer_rating` in particular introduces data leakage, since it's only
known after delivery). The deployed **Stacking Classifier** (Random Forest +
Decision Tree base learners → Logistic Regression meta-learner) achieved the
best held-out **F1 Score of 0.7157**, ahead of tuned AdaBoost and XGBoost.

---

## 🚀 Getting Started

### 1. Clone and install

```bash
git clone <your-repo-url>
cd shipping-delay-prediction
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add your trained artifacts

Copy the following files from your training environment into their
respective folders (see each folder's `README.md` for details):

```
models/shipping_delay_model.pkl
models/scaler.pkl
models/warehouse_encoder.pkl
models/shipment_encoder.pkl
models/importance_encoder.pkl
data/cleaned.csv
graphs/*.png            # optional
```

### 3. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

> If model or data files are missing, the app still runs — affected pages
> show a clear notice explaining what to add instead of crashing.

---

## ☁️ Deploying to Streamlit Community Cloud

1. Push this repository to GitHub (including your `data/` and `models/`
   files — Streamlit Cloud needs them at runtime; there's no separate
   file-upload step for the base app).
2. Go to [share.streamlit.io](https://share.streamlit.io), connect your
   GitHub account, and select this repo.
3. Set the main file path to `app.py`.
4. Deploy — no additional configuration required. All paths in the code are
   relative to the project root, so it works unmodified in the cloud.

---

## 🛠️ Tech Stack

- **Streamlit** — application framework & UI
- **scikit-learn** — StandardScaler, LabelEncoder, RandomForest, Stacking, etc.
- **XGBoost** — gradient boosting comparison model
- **Plotly** — interactive gauges and charts
- **Pandas / NumPy** — data handling
- **joblib** — model & encoder persistence

---

## 📈 Model Leaderboard (F1 Score)

| Rank | Model | F1 Score |
|---|---|---|
| 1 | **Stacking Classifier** ✅ deployed | **0.7157** |
| 2 | AdaBoost (tuned) | 0.7051 |
| 3 | XGBoost (tuned) | 0.7030 |

Full comparison across all 10 models (Logistic Regression, KNN, SVM,
Gaussian Naive Bayes, Decision Tree, Random Forest, AdaBoost, Gradient
Boosting, XGBoost, Stacking Classifier) is available in the notebook and
in the app's **Model Info** page.

---

## 📄 License

This project is provided as-is for portfolio and educational use.
