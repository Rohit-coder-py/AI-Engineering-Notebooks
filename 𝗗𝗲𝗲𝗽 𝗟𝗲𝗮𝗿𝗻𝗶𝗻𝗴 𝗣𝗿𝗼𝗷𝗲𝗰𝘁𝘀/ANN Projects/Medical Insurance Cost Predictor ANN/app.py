import os
import sys

import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from inference import predict

st.set_page_config(page_title="Medical Insurance Cost Predictor", page_icon="🏥", layout="wide")

st.title("Medical Insurance Cost Predictor")
st.write("Fill in the details below to estimate the annual medical cost using the trained ANN model.")

model_path = os.path.join(os.path.dirname(__file__), "models", "medical_insurance_ann.pth")
if not os.path.exists(model_path):
    st.warning("Model file not found in models/. Train the model first using src/train.py")

with st.form("prediction_form"):

    st.subheader("Demographic & Personal Information")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        age = st.number_input("Age", min_value=0, max_value=100, value=40)
        sex = st.selectbox("Sex", ["Female", "Male", "Other"])
    with c2:
        region = st.selectbox("Region", ["North", "South", "East", "West", "Central"])
        urban_rural = st.selectbox("Urban / Rural", ["Urban", "Suburban", "Rural"])
    with c3:
        income = st.number_input("Annual Income", min_value=0, value=50000, step=1000)
        education = st.selectbox("Education", ["No HS", "HS", "Some College", "Bachelors", "Masters", "Doctorate"])
    with c4:
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
        employment_status = st.selectbox("Employment Status", ["Employed", "Self-employed", "Unemployed", "Retired"])

    c5, c6 = st.columns(2)
    with c5:
        household_size = st.number_input("Household Size", min_value=1, max_value=15, value=3)
    with c6:
        dependents = st.number_input("Dependents", min_value=0, max_value=10, value=1)

    st.subheader("Health & Lifestyle")
    c7, c8, c9 = st.columns(3)
    with c7:
        bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=27.0, step=0.1)
        smoker = st.selectbox("Smoker", ["Never", "Former", "Current"])
    with c8:
        visits_last_year = st.number_input("Visits Last Year", min_value=0, max_value=30, value=2)
        hospitalizations_last_3yrs = st.number_input("Hospitalizations (Last 3 yrs)", min_value=0, max_value=10, value=0)
    with c9:
        days_hospitalized_last_3yrs = st.number_input("Days Hospitalized (Last 3 yrs)", min_value=0, max_value=60, value=0)
        medication_count = st.number_input("Medication Count", min_value=0, max_value=20, value=1)

    st.subheader("Clinical Measurements")
    c10, c11, c12, c13 = st.columns(4)
    with c10:
        systolic_bp = st.number_input("Systolic BP", min_value=60.0, max_value=220.0, value=118.0)
    with c11:
        diastolic_bp = st.number_input("Diastolic BP", min_value=40.0, max_value=140.0, value=74.0)
    with c12:
        ldl = st.number_input("LDL", min_value=20.0, max_value=300.0, value=120.0)
    with c13:
        hba1c = st.number_input("HbA1c", min_value=3.0, max_value=15.0, value=5.6, step=0.1)

    st.subheader("Insurance Policy Information")
    c14, c15, c16, c17 = st.columns(4)
    with c14:
        plan_type = st.selectbox("Plan Type", ["PPO", "POS", "HMO", "EPO"])
        network_tier = st.selectbox("Network Tier", ["Bronze", "Silver", "Gold", "Platinum"])
    with c15:
        deductible = st.number_input("Deductible", min_value=0, max_value=10000, value=1200, step=100)
        copay = st.number_input("Copay", min_value=0, max_value=200, value=20)
    with c16:
        policy_term_years = st.number_input("Policy Term (Years)", min_value=1, max_value=20, value=5)
        policy_changes_last_2yrs = st.number_input("Policy Changes (Last 2 yrs)", min_value=0, max_value=10, value=0)
    with c17:
        provider_quality = st.number_input("Provider Quality (1-5)", min_value=1.0, max_value=5.0, value=3.6, step=0.1)

    st.subheader("Chronic Medical Conditions")
    c18, c19, c20, c21, c22 = st.columns(5)
    with c18:
        chronic_count = st.number_input("Chronic Condition Count", min_value=0, max_value=10, value=0)
        hypertension = st.checkbox("Hypertension")
    with c19:
        diabetes = st.checkbox("Diabetes")
        asthma = st.checkbox("Asthma")
    with c20:
        copd = st.checkbox("COPD")
        cardiovascular_disease = st.checkbox("Cardiovascular Disease")
    with c21:
        cancer_history = st.checkbox("Cancer History")
        kidney_disease = st.checkbox("Kidney Disease")
    with c22:
        liver_disease = st.checkbox("Liver Disease")
        arthritis = st.checkbox("Arthritis")
    mental_health = st.checkbox("Mental Health Condition")

    st.subheader("Medical Procedures")
    c23, c24, c25, c26, c27 = st.columns(5)
    with c23:
        proc_imaging_count = st.number_input("Imaging Procedures", min_value=0, max_value=20, value=0)
    with c24:
        proc_surgery_count = st.number_input("Surgery Procedures", min_value=0, max_value=20, value=0)
    with c25:
        proc_physio_count = st.number_input("Physio Sessions", min_value=0, max_value=20, value=0)
    with c26:
        proc_consult_count = st.number_input("Consultations", min_value=0, max_value=20, value=0)
    with c27:
        proc_lab_count = st.number_input("Lab Tests", min_value=0, max_value=20, value=0)

    submitted = st.form_submit_button("Predict Annual Medical Cost")

if submitted:
    raw_input = {
        "age": age,
        "sex": sex,
        "region": region,
        "urban_rural": urban_rural,
        "income": income,
        "education": education,
        "marital_status": marital_status,
        "employment_status": employment_status,
        "household_size": household_size,
        "dependents": dependents,
        "bmi": bmi,
        "smoker": smoker,
        "visits_last_year": visits_last_year,
        "hospitalizations_last_3yrs": hospitalizations_last_3yrs,
        "days_hospitalized_last_3yrs": days_hospitalized_last_3yrs,
        "medication_count": medication_count,
        "systolic_bp": systolic_bp,
        "diastolic_bp": diastolic_bp,
        "ldl": ldl,
        "hba1c": hba1c,
        "plan_type": plan_type,
        "network_tier": network_tier,
        "deductible": deductible,
        "copay": copay,
        "policy_term_years": policy_term_years,
        "policy_changes_last_2yrs": policy_changes_last_2yrs,
        "provider_quality": provider_quality,
        "chronic_count": chronic_count,
        "hypertension": int(hypertension),
        "diabetes": int(diabetes),
        "asthma": int(asthma),
        "copd": int(copd),
        "cardiovascular_disease": int(cardiovascular_disease),
        "cancer_history": int(cancer_history),
        "kidney_disease": int(kidney_disease),
        "liver_disease": int(liver_disease),
        "arthritis": int(arthritis),
        "mental_health": int(mental_health),
        "proc_imaging_count": proc_imaging_count,
        "proc_surgery_count": proc_surgery_count,
        "proc_physio_count": proc_physio_count,
        "proc_consult_count": proc_consult_count,
        "proc_lab_count": proc_lab_count,
    }

    try:
        prediction = predict(raw_input)
        st.success(f"Estimated Annual Medical Cost: ₹ {prediction:,.2f}")
    except FileNotFoundError:
        st.error("Model or artifacts not found. Please run src/train.py first to train the model and generate artifacts.")
