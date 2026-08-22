
import os
import sys
import json
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from infer import load_model, predict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Smartphone Addiction Risk",
    page_icon="📵",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Dark editorial theme
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,500&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"]  {
    background-color: #0d0f14 !important;
    color: #e7e2d6 !important;
    font-family: 'JetBrains Mono', monospace;
}
.stApp { background-color: #0d0f14; }

h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #c9a86a !important;
    letter-spacing: 0.02em;
}
h1 { font-size: 2.6rem !important; font-weight: 600 !important; }

.subtitle {
    color: #9a9488;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

div[data-testid="stMetric"] {
    background-color: #161923;
    border: 1px solid #3a3f4d;
    padding: 1rem;
    border-radius: 4px;
}

.risk-card {
    padding: 1.6rem 2rem;
    border-radius: 6px;
    margin-top: 1.5rem;
    border: 1px solid #3a3f4d;
    font-family: 'JetBrains Mono', monospace;
}
.risk-low { background: linear-gradient(135deg, #16231e, #161923); border-color: #2f6f5e; }
.risk-moderate { background: linear-gradient(135deg, #231f16, #161923); border-color: #c9a86a; }
.risk-high { background: linear-gradient(135deg, #231616, #161923); border-color: #7a2e2e; }

.risk-label {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-weight: 600;
}
.stButton>button {
    background-color: #c9a86a;
    color: #0d0f14;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    border: none;
    padding: 0.6rem 1.4rem;
    border-radius: 4px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.stButton>button:hover { background-color: #e0c088; }

hr { border-color: #2a2e3a; }
</style>
""", unsafe_allow_html=True)

st.title("Smartphone Addiction Risk")
st.markdown('<div class="subtitle">Behavioural Screening · PyTorch ANN</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Load model (cached)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_model():
    return load_model()

try:
    model, scaler, encoders, feature_order = get_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error(f"Could not load model artifacts. Run `python src/train.py` first.\n\n{e}")

# ---------------------------------------------------------------------------
# Input form
# ---------------------------------------------------------------------------
if model_loaded:
    with st.form("input_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.slider("Age", 18, 35, 22)
            daily_screen_time_hours = st.slider("Daily screen time (hrs)", 3.0, 12.0, 6.5, 0.1)
            social_media_hours = st.slider("Social media (hrs)", 0.5, 6.0, 2.5, 0.1)
            gaming_hours = st.slider("Gaming (hrs)", 0.0, 4.0, 1.5, 0.1)
            weekend_screen_time = st.slider("Weekend screen time (hrs)", 3.5, 15.0, 8.0, 0.1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        with col2:
            work_study_hours = st.slider("Work/study (hrs)", 0.5, 6.0, 3.0, 0.1)
            sleep_hours = st.slider("Sleep (hrs)", 4.5, 9.0, 6.7, 0.1)
            notifications_per_day = st.slider("Notifications/day", 20, 250, 130)
            app_opens_per_day = st.slider("App opens/day", 15, 180, 95)
            stress_level = st.selectbox("Stress level", ["Low", "Medium", "High"])
            academic_work_impact = st.selectbox("Academic/work impact reported?", ["No", "Yes"])

        submitted = st.form_submit_button("Predict Risk")

    if submitted:
        raw_input = {
            "age": age,
            "daily_screen_time_hours": daily_screen_time_hours,
            "social_media_hours": social_media_hours,
            "gaming_hours": gaming_hours,
            "work_study_hours": work_study_hours,
            "sleep_hours": sleep_hours,
            "notifications_per_day": notifications_per_day,
            "app_opens_per_day": app_opens_per_day,
            "weekend_screen_time": weekend_screen_time,
            "gender": gender,
            "stress_level": stress_level,
            "academic_work_impact": academic_work_impact,
        }

        try:
            result = predict(raw_input, model, scaler, encoders, feature_order)

            tier_class = {
                "Low": "risk-low", "Moderate": "risk-moderate", "High": "risk-high"
            }[result["risk_tier"]]

            st.markdown(f"""
            <div class="risk-card {tier_class}">
                <div class="subtitle">Predicted Risk Tier</div>
                <div class="risk-label">{result['risk_tier']}</div>
                <div style="margin-top:0.5rem; color:#9a9488;">
                    Probability of addictive usage pattern: <b style="color:#e7e2d6;">{result['probability']*100:.1f}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.caption(
                "This is a screening estimate based on self-reported usage patterns, "
                "not a clinical diagnosis. If screen use is affecting sleep, work, or "
                "wellbeing, consider speaking with a professional."
            )
        except Exception as e:
            st.error(f"Prediction failed: {e}")

# ---------------------------------------------------------------------------
# Model metrics footer
# ---------------------------------------------------------------------------
metrics_path = os.path.join(ROOT, "models", "metrics.json")
if os.path.exists(metrics_path):
    with open(metrics_path) as f:
        metrics = json.load(f)
    st.markdown("---")
    st.markdown('<div class="subtitle">Model Performance (Held-out Test Set)</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy", f"{metrics['accuracy']*100:.1f}%")
    m2.metric("Precision", f"{metrics['precision']*100:.1f}%")
    m3.metric("Recall", f"{metrics['recall']*100:.1f}%")
    m4.metric("F1 Score", f"{metrics['f1']*100:.1f}%")
