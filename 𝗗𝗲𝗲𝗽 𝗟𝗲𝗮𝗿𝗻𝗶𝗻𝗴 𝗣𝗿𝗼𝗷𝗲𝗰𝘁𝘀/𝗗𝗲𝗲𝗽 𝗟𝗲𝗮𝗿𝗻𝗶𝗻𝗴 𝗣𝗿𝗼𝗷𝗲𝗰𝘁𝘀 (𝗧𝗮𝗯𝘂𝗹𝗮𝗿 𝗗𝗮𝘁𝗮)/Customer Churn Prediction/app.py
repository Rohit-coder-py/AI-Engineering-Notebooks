"""
Simple Streamlit UI for the Customer Churn Prediction model.

Run with:
    streamlit run app/app.py
"""

import os
import sys

import streamlit as st

# make src/ importable no matter where streamlit is launched from
APP_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(os.path.dirname(APP_DIR), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from infer import predict  # noqa: E402

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📉",
    layout="centered",
)

# ---- force a clean light look regardless of the visitor's system theme ----
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

    except FileNotFoundError:
        st.error(
            "Model artifacts not found in `models/`. Run `python src/train.py` "
            "first to train and save the model."
        )

st.divider()
st.caption(
    "Trained on the Telco Customer Churn dataset with a PyTorch ANN "
    "(30 → 64 → 32 → 16 → 1). For portfolio / demo purposes."
)
