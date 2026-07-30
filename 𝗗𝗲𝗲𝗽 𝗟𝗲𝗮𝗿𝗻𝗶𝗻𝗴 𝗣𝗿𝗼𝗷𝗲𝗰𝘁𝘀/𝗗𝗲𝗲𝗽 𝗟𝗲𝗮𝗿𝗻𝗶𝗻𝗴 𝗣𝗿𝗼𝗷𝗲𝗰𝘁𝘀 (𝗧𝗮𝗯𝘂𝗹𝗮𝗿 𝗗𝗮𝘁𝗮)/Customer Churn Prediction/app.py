"""
Customer Churn Prediction — single-file Streamlit app.

Run with:
    streamlit run app.py

Everything the app needs (model architecture, preprocessing, inference,
and UI) lives in this one file so it can be deployed as-is (e.g. on
Streamlit Community Cloud) with no `src/` package or path juggling.

Expected folder layout next to this file:
    models/churn_model_weights.npz
    models/scaler.pkl
    models/feature_order.pkl
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import torch
import torch.nn as nn

# --------------------------------------------------------------------------
# Paths — resolved relative to this file, so it works no matter which
# directory `streamlit run` is launched from (local machine or a cloud host).
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
SCALER_PATH = MODELS_DIR / "scaler.pkl"
FEATURE_ORDER_PATH = MODELS_DIR / "feature_order.pkl"
WEIGHTS_PATH = MODELS_DIR / "churn_model_weights.npz"
METRICS_PATH = MODELS_DIR / "metrics.json"


# ==========================================================================
# Model architecture — must match the one the weights were trained with.
# ==========================================================================
class MyModel(nn.Module):
    def __init__(self, n_features: int = 30):
        super().__init__()
        self.fc1 = nn.Linear(n_features, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 16)
        self.fc4 = nn.Linear(16, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.fc4(x)
        return x


# ==========================================================================
# Preprocessing — turns a raw form submission into the exact encoded row
# the model was trained on (LabelEncoder-style binary mapping for yes/no
# columns, one-hot with drop_first for multi-category columns).
# ==========================================================================
BINARY_MAP = {
    "gender": {"Female": 0, "Male": 1},
    "Partner": {"No": 0, "Yes": 1},
    "Dependents": {"No": 0, "Yes": 1},
    "PhoneService": {"No": 0, "Yes": 1},
    "PaperlessBilling": {"No": 0, "Yes": 1},
}

MULTI_COLS = [
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaymentMethod",
]


def build_feature_row(raw: dict, feature_order: list[str]) -> pd.DataFrame:
    """Encode a single raw customer record into a 1-row DataFrame whose
    columns exactly match `feature_order` (the column order the scaler
    and model were fit on)."""
    row: dict[str, float] = {}

    for col, mapping in BINARY_MAP.items():
        row[col] = mapping[raw[col]]

    row["SeniorCitizen"] = int(raw["SeniorCitizen"])
    row["tenure"] = float(raw["tenure"])
    row["MonthlyCharges"] = float(raw["MonthlyCharges"])
    row["TotalCharges"] = float(raw["TotalCharges"])

    # every one-hot column starts at 0, then we flip on the matching one
    one_hot_cols = [c for c in feature_order if c not in row]
    for c in one_hot_cols:
        row[c] = 0

    for col in MULTI_COLS:
        dummy_name = f"{col}_{raw[col]}"
        if dummy_name in row:
            row[dummy_name] = 1
        # otherwise it's the dropped baseline category — every dummy for
        # that column correctly stays 0, matching pd.get_dummies(drop_first=True)

    df_row = pd.DataFrame([row])
    return df_row[feature_order]


# ==========================================================================
# Artifact loading — cached so the model/scaler are only loaded once per
# session, not on every form submission.
# ==========================================================================
@st.cache_resource(show_spinner=False)
def load_artifacts():
    if not (SCALER_PATH.exists() and FEATURE_ORDER_PATH.exists() and WEIGHTS_PATH.exists()):
        missing = [
            str(p.relative_to(BASE_DIR))
            for p in (SCALER_PATH, FEATURE_ORDER_PATH, WEIGHTS_PATH)
            if not p.exists()
        ]
        raise FileNotFoundError(
            "Missing model artifact(s): " + ", ".join(missing)
        )

    scaler = joblib.load(SCALER_PATH)
    feature_order = joblib.load(FEATURE_ORDER_PATH)

    weights = np.load(WEIGHTS_PATH)
    model = MyModel(n_features=len(feature_order))
    state_dict = {k: torch.tensor(weights[k]) for k in weights.files}
    model.load_state_dict(state_dict)
    model.eval()

    return model, scaler, feature_order


@st.cache_data(show_spinner=False)
def load_metrics() -> dict | None:
    if METRICS_PATH.exists():
        with open(METRICS_PATH) as f:
            return json.load(f)
    return None


def predict(raw: dict) -> dict:
    model, scaler, feature_order = load_artifacts()

    row_df = build_feature_row(raw, feature_order)
    row_scaled = scaler.transform(row_df)
    row_tensor = torch.tensor(row_scaled, dtype=torch.float32)

    with torch.no_grad():
        logit = model(row_tensor)
        prob = torch.sigmoid(logit).item()

    return {
        "churn_probability": prob,
        "churn_prediction": int(prob >= 0.5),
    }


# ==========================================================================
# UI
# ==========================================================================
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📉",
    layout="centered",
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #ffffff;
            color: #1f2937;
        }
        .main .block-container {
            padding-top: 2rem;
            max-width: 780px;
        }
        h1, h2, h3 {
            color: #111827;
        }
        .result-card {
            padding: 1.25rem 1.5rem;
            border-radius: 12px;
            margin-top: 1rem;
            border: 1px solid #e5e7eb;
        }
        .result-churn {
            background-color: #fef2f2;
            border-color: #fecaca;
        }
        .result-stay {
            background-color: #f0fdf4;
            border-color: #bbf7d0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📉 Customer Churn Prediction")
st.write(
    "Fill in a customer's details and the model will estimate how likely "
    "they are to churn (cancel their subscription)."
)

metrics = load_metrics()
if metrics:
    with st.expander("Model performance (held-out test set)"):
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Accuracy", f"{metrics['accuracy']:.1%}")
        c2.metric("Precision", f"{metrics['precision']:.1%}")
        c3.metric("Recall", f"{metrics['recall']:.1%}")
        c4.metric("F1", f"{metrics['f1_score']:.1%}")
        c5.metric("ROC-AUC", f"{metrics['roc_auc']:.3f}")

st.divider()

with st.form("churn_form"):
    st.subheader("Customer Profile")

    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner = st.selectbox("Has Partner", ["No", "Yes"])
        dependents = st.selectbox("Has Dependents", ["No", "Yes"])
    with col2:
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=70.0, step=1.0)
        total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=840.0, step=10.0)
        paperless_billing = st.selectbox("Paperless Billing", ["No", "Yes"])

    st.subheader("Services")

    col3, col4 = st.columns(2)
    with col3:
        phone_service = st.selectbox("Phone Service", ["No", "Yes"])
        multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
    with col4:
        device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])

    st.subheader("Account")

    col5, col6 = st.columns(2)
    with col5:
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    with col6:
        payment_method = st.selectbox(
            "Payment Method",
            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
        )

    submitted = st.form_submit_button("Predict Churn", use_container_width=True)

if submitted:
    raw_input = {
        "gender": gender,
        "SeniorCitizen": 1 if senior_citizen == "Yes" else 0,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
    }

    # a couple of light, honest data-consistency nudges (non-blocking)
    if phone_service == "No" and multiple_lines != "No phone service":
        st.warning("Phone Service is 'No' — Multiple Lines is usually 'No phone service' in that case.")
    if internet_service == "No":
        internet_dependent = [online_security, online_backup, device_protection,
                               tech_support, streaming_tv, streaming_movies]
        if any(v != "No internet service" for v in internet_dependent):
            st.warning("Internet Service is 'No' — the internet-dependent options below it "
                       "are usually 'No internet service' in that case.")

    try:
        result = predict(raw_input)
        prob = result["churn_probability"]
        pred = result["churn_prediction"]

        if pred == 1:
            st.markdown(
                f"""
                <div class="result-card result-churn">
                    <h3>⚠️ Likely to Churn</h3>
                    <p>Estimated churn probability: <b>{prob * 100:.1f}%</b></p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="result-card result-stay">
                    <h3>✅ Likely to Stay</h3>
                    <p>Estimated churn probability: <b>{prob * 100:.1f}%</b></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.progress(min(max(prob, 0.0), 1.0))

    except FileNotFoundError as e:
        st.error(
            f"Model artifacts not found ({e}). Make sure the `models/` folder "
            "(scaler.pkl, feature_order.pkl, churn_model_weights.npz) is deployed "
            "alongside app.py."
        )

st.divider()
st.caption(
    "Trained on the Telco Customer Churn dataset with a PyTorch ANN "
    "(30 → 64 → 32 → 16 → 1). For portfolio / demo purposes."
)
