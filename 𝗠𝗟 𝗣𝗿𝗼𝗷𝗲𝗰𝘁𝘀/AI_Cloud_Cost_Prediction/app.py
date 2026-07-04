import pickle
import datetime as dt

import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Cloud Cost Predictor",
    page_icon="▲",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# Load artifacts
# ----------------------------------------------------------------------------
@st.cache_resource
def load_artifacts():
    with open("models/linear_regression_pipeline.pkl", "rb") as f:
        pipeline = pickle.load(f)
    with open("models/feature_schema.pkl", "rb") as f:
        schema = pickle.load(f)
    with open("models/category_options.pkl", "rb") as f:
        options = pickle.load(f)
    return pipeline, schema, options


pipeline, schema, category_options = load_artifacts()

# ----------------------------------------------------------------------------
# Design tokens — dark cloud-console aesthetic
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

    :root {
        --bg:        #0B0E14;
        --surface:   #12161F;
        --surface-2: #171C27;
        --border:    #232838;
        --text:      #E8EAED;
        --muted:     #8B93A7;
        --accent:    #5EEAD4;
        --accent-dim: rgba(94, 234, 212, 0.12);
        --warn:      #F59E0B;
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: var(--bg); color: var(--text); }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container { padding-top: 2.5rem; max-width: 1100px; }

    /* Header */
    .app-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 0.4rem;
    }
    .app-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: var(--text);
        margin: 0 0 0.35rem 0;
        letter-spacing: -0.02em;
    }
    .app-subtitle {
        color: var(--muted);
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    /* Panels */
    .panel {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1.6rem 1.8rem;
    }
    .panel-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 1rem;
    }

    /* Ledger / readout */
    .ledger {
        background: var(--surface-2);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1.8rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .ledger-row {
        display: flex;
        justify-content: space-between;
        padding: 0.4rem 0;
        font-size: 0.82rem;
        color: var(--muted);
        border-bottom: 1px dashed var(--border);
    }
    .ledger-row span:last-child { color: var(--text); }
    .ledger-row:last-of-type { border-bottom: none; }

    .readout-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--muted);
        margin-top: 1.6rem;
    }
    .readout-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 3rem;
        font-weight: 700;
        color: var(--accent);
        line-height: 1.1;
        margin: 0.2rem 0 0.4rem 0;
    }
    .readout-caption {
        color: var(--muted);
        font-size: 0.78rem;
    }

    /* Streamlit widget overrides */
    div[data-baseweb="select"] > div, .stNumberInput input, .stDateInput input {
        background-color: var(--surface-2) !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif;
    }
    label { color: var(--muted) !important; font-size: 0.82rem !important; }

    .stButton > button {
        background: var(--accent);
        color: #06110F;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.4rem;
        width: 100%;
        font-family: 'Inter', sans-serif;
        transition: opacity 0.15s ease;
    }
    .stButton > button:hover { opacity: 0.85; color: #06110F; }

    hr { border-color: var(--border); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown('<div class="app-eyebrow">Azure · Cost Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="app-title">Cloud Cost Predictor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Estimate the billing cost of a line item before it hits your invoice — trained on historical Azure consumption data.</div>',
    unsafe_allow_html=True,
)

col_input, col_output = st.columns([1.15, 1], gap="large")

# ----------------------------------------------------------------------------
# Input panel
# ----------------------------------------------------------------------------
with col_input:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-label">Billing Line Item</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        meter_category = st.selectbox("Service category", category_options["MeterCategory"])
        resource_location = st.selectbox("Region", category_options["ResourceLocation"])
    with c2:
        consumed_service = st.selectbox("Consumed service", category_options["ConsumedService"])
        billing_date = st.date_input("Billing date", value=dt.date.today())

    meter_sub_category = st.selectbox("Meter sub-category", category_options["MeterSubCategory"])
    meter_name = st.selectbox("Meter name", category_options["MeterName"])

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    predict_clicked = st.button("Predict cost")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Output panel
# ----------------------------------------------------------------------------
with col_output:
    st.markdown('<div class="ledger">', unsafe_allow_html=True)
    st.markdown('<div class="panel-label">Predicted Line Item</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="ledger-row"><span>Service category</span><span>{meter_category}</span></div>
        <div class="ledger-row"><span>Consumed service</span><span>{consumed_service}</span></div>
        <div class="ledger-row"><span>Region</span><span>{resource_location}</span></div>
        <div class="ledger-row"><span>Meter sub-category</span><span>{meter_sub_category}</span></div>
        <div class="ledger-row"><span>Meter name</span><span>{meter_name}</span></div>
        <div class="ledger-row"><span>Date</span><span>{billing_date.strftime('%Y-%m-%d')}</span></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="readout-label">Estimated Cost</div>', unsafe_allow_html=True)

    if predict_clicked:
        input_row = pd.DataFrame([{
            "Year": billing_date.year,
            "Month": billing_date.month,
            "Day": billing_date.day,
            "Weekday": billing_date.weekday(),
            "MeterCategory": meter_category,
            "ConsumedService": consumed_service,
            "ResourceLocation": resource_location,
            "MeterSubCategory": meter_sub_category,
            "MeterName": meter_name,
        }])[schema["all_features_in_order"]]

        prediction = float(pipeline.predict(input_row)[0])
        prediction = max(prediction, 0.0)  # cost can't be negative

        st.markdown(f'<div class="readout-value">${prediction:,.4f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="readout-caption">Predicted CostInBillingCurrency for this billing line item</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="readout-value">$ —.——</div>', unsafe_allow_html=True)
        st.markdown('<div class="readout-caption">Fill in the fields and press Predict cost</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
st.caption("Model: Linear Regression (scikit-learn Pipeline) · Trained on anonymized Azure billing data · For estimation purposes only")
