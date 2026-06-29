"""
Employee Attrition Prediction & HR Analytics System
=====================================================
Author  : Harsh Jha
Model   : Support Vector Machine (SVM) — C=0.1, kernel=linear, gamma=scale
Dataset : IBM HR Analytics Employee Attrition dataset (encoded)
"""

import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Employee Attrition Prediction | HR Analytics",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# PATHS  — adjust only these two lines if you move the files
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR  = os.path.join(BASE_DIR, "..", "models")

MODEL_PATH  = os.path.join(MODEL_DIR, "employee_attrition_svm.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "employee_attrition_scaler.pkl")

# ─────────────────────────────────────────────────────────────────────────────
# EXACT feature order used during training (inferred from encoded dataset)
# ─────────────────────────────────────────────────────────────────────────────
FEATURE_COLUMNS = [
    "Age", "DailyRate", "DistanceFromHome", "Education",
    "EnvironmentSatisfaction", "Gender", "HourlyRate", "JobInvolvement",
    "JobLevel", "JobSatisfaction", "MonthlyIncome", "MonthlyRate",
    "NumCompaniesWorked", "OverTime", "PercentSalaryHike", "PerformanceRating",
    "RelationshipSatisfaction", "StockOptionLevel", "TotalWorkingYears",
    "TrainingTimesLastYear", "WorkLifeBalance", "YearsAtCompany",
    "YearsInCurrentRole", "YearsSinceLastPromotion", "YearsWithCurrManager",
    # One-hot encoded: BusinessTravel (drop = Non-Travel)
    "BusinessTravel_Travel_Frequently", "BusinessTravel_Travel_Rarely",
    # One-hot encoded: Department (drop = Human Resources)
    "Department_Research & Development", "Department_Sales",
    # One-hot encoded: EducationField (drop = Human Resources field)
    "EducationField_Life Sciences", "EducationField_Marketing",
    "EducationField_Medical", "EducationField_Other",
    "EducationField_Technical Degree",
    # One-hot encoded: JobRole (drop = Healthcare Representative)
    "JobRole_Human Resources", "JobRole_Laboratory Technician",
    "JobRole_Manager", "JobRole_Manufacturing Director",
    "JobRole_Research Director", "JobRole_Research Scientist",
    "JobRole_Sales Executive", "JobRole_Sales Representative",
    # One-hot encoded: MaritalStatus (drop = Divorced)
    "MaritalStatus_Married", "MaritalStatus_Single",
]


# ─────────────────────────────────────────────────────────────────────────────
# MODEL LOADING  (cached so it only loads once per session)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading model…")
def load_model():
    """Load the trained SVM model and its scaler from disk."""
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)
    return model, scaler


# ─────────────────────────────────────────────────────────────────────────────
# FEATURE ENGINEERING  — converts raw user inputs → encoded DataFrame
# ─────────────────────────────────────────────────────────────────────────────
def preprocess_input(raw: dict) -> pd.DataFrame:
    """
    Convert the human-friendly form inputs into a single-row DataFrame
    whose columns exactly match FEATURE_COLUMNS (training order preserved).

    Parameters
    ----------
    raw : dict
        Keys are the readable widget names collected from the Streamlit form.

    Returns
    -------
    pd.DataFrame
        Shape (1, 44) — ready for scaler.transform().
    """
    row = {col: 0 for col in FEATURE_COLUMNS}

    # ── Numeric / ordinal features (pass through directly) ──────────────────
    numeric_map = {
        "Age":                    raw["Age"],
        "DailyRate":              raw["DailyRate"],
        "DistanceFromHome":       raw["DistanceFromHome"],
        "Education":              raw["Education"],
        "EnvironmentSatisfaction":raw["EnvironmentSatisfaction"],
        "HourlyRate":             raw["HourlyRate"],
        "JobInvolvement":         raw["JobInvolvement"],
        "JobLevel":               raw["JobLevel"],
        "JobSatisfaction":        raw["JobSatisfaction"],
        "MonthlyIncome":          raw["MonthlyIncome"],
        "MonthlyRate":            raw["MonthlyRate"],
        "NumCompaniesWorked":     raw["NumCompaniesWorked"],
        "PercentSalaryHike":      raw["PercentSalaryHike"],
        "PerformanceRating":      raw["PerformanceRating"],
        "RelationshipSatisfaction":raw["RelationshipSatisfaction"],
        "StockOptionLevel":       raw["StockOptionLevel"],
        "TotalWorkingYears":      raw["TotalWorkingYears"],
        "TrainingTimesLastYear":  raw["TrainingTimesLastYear"],
        "WorkLifeBalance":        raw["WorkLifeBalance"],
        "YearsAtCompany":         raw["YearsAtCompany"],
        "YearsInCurrentRole":     raw["YearsInCurrentRole"],
        "YearsSinceLastPromotion":raw["YearsSinceLastPromotion"],
        "YearsWithCurrManager":   raw["YearsWithCurrManager"],
    }
    row.update(numeric_map)

    # ── Binary features ──────────────────────────────────────────────────────
    row["Gender"]   = 1 if raw["Gender"]  == "Male" else 0          # Male=1
    row["OverTime"] = 1 if raw["OverTime"] == "Yes" else 0

    # ── One-hot: BusinessTravel (reference = Non-Travel) ────────────────────
    bt = raw["BusinessTravel"]
    row["BusinessTravel_Travel_Frequently"] = 1 if bt == "Travel_Frequently" else 0
    row["BusinessTravel_Travel_Rarely"]     = 1 if bt == "Travel_Rarely"     else 0

    # ── One-hot: Department (reference = Human Resources) ───────────────────
    dept = raw["Department"]
    row["Department_Research & Development"] = 1 if dept == "Research & Development" else 0
    row["Department_Sales"]                  = 1 if dept == "Sales"                  else 0

    # ── One-hot: EducationField (reference = Human Resources field) ─────────
    ef = raw["EducationField"]
    row["EducationField_Life Sciences"]     = 1 if ef == "Life Sciences"     else 0
    row["EducationField_Marketing"]         = 1 if ef == "Marketing"         else 0
    row["EducationField_Medical"]           = 1 if ef == "Medical"           else 0
    row["EducationField_Other"]             = 1 if ef == "Other"             else 0
    row["EducationField_Technical Degree"]  = 1 if ef == "Technical Degree"  else 0

    # ── One-hot: JobRole (reference = Healthcare Representative) ────────────
    jr = raw["JobRole"]
    row["JobRole_Human Resources"]         = 1 if jr == "Human Resources"         else 0
    row["JobRole_Laboratory Technician"]   = 1 if jr == "Laboratory Technician"   else 0
    row["JobRole_Manager"]                 = 1 if jr == "Manager"                 else 0
    row["JobRole_Manufacturing Director"]  = 1 if jr == "Manufacturing Director"  else 0
    row["JobRole_Research Director"]       = 1 if jr == "Research Director"       else 0
    row["JobRole_Research Scientist"]      = 1 if jr == "Research Scientist"      else 0
    row["JobRole_Sales Executive"]         = 1 if jr == "Sales Executive"         else 0
    row["JobRole_Sales Representative"]    = 1 if jr == "Sales Representative"    else 0

    # ── One-hot: MaritalStatus (reference = Divorced) ───────────────────────
    ms = raw["MaritalStatus"]
    row["MaritalStatus_Married"] = 1 if ms == "Married" else 0
    row["MaritalStatus_Single"]  = 1 if ms == "Single"  else 0

    return pd.DataFrame([row], columns=FEATURE_COLUMNS)


# ─────────────────────────────────────────────────────────────────────────────
# PREDICTION
# ─────────────────────────────────────────────────────────────────────────────
def predict(model, scaler, input_df: pd.DataFrame):
    """
    Scale the input and run inference.

    Returns
    -------
    prediction : int   — 0 (Stay) or 1 (Leave)
    confidence : float — decision function score (higher = more confident)
    """
    X_scaled    = scaler.transform(input_df)
    prediction  = int(model.predict(X_scaled)[0])

    # SVM with kernel='linear' and C=0.1 does NOT enable predict_proba by
    # default (requires probability=True at fit time).  We use the signed
    # distance from the decision hyperplane as a confidence proxy instead.
    decision_score = float(model.decision_function(X_scaled)[0])

    return prediction, decision_score


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS  — light professional styling that works in both themes
# ─────────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        /* Header gradient banner */
        .hero-banner {
            background: linear-gradient(135deg, #1f3c88 0%, #357abd 100%);
            border-radius: 12px;
            padding: 2rem 2.5rem;
            color: white;
            margin-bottom: 1.5rem;
        }
        .hero-banner h1 { margin: 0 0 .3rem 0; font-size: 2.2rem; }
        .hero-banner p  { margin: 0; opacity: .88; font-size: 1rem; }

        /* Section card */
        .section-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 10px;
            padding: 1.2rem 1.5rem;
            margin-bottom: 1.2rem;
        }
        .section-card h4 { margin-top: 0; color: #357abd; font-size: 1rem;
                           letter-spacing: .05em; text-transform: uppercase; }

        /* Confidence badge */
        .conf-badge {
            display: inline-block;
            padding: .35rem .85rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: .95rem;
        }
        .conf-high   { background: #d4edda; color: #155724; }
        .conf-medium { background: #fff3cd; color: #856404; }
        .conf-low    { background: #f8d7da; color: #721c24; }

        /* Sidebar styling */
        section[data-testid="stSidebar"] { background-color: #0f2248; }
        section[data-testid="stSidebar"] * { color: #d0dff5 !important; }
        section[data-testid="stSidebar"] .stMarkdown h3 { color: #7eb3ff !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.image(
            "https://img.icons8.com/fluency/96/group.png",
            width=72,
        )
        st.markdown("## HR Analytics System")
        st.markdown("---")
        st.markdown("### 📌 Project Info")
        st.markdown(
            """
            **Project**  
            Employee Attrition Prediction

            **Algorithm**  
            Support Vector Machine (SVM)

            **Kernel**  
            Linear

            **Best Parameters**  
            `C=0.1 | kernel=linear | gamma=scale`
            """
        )
        st.markdown("---")
        st.markdown("### Developer")
        st.markdown("*Rohit Jha*  \n*ML Engineer*")
        st.markdown("---")
        st.caption(
            "This tool is intended to *assist* HR decisions — "
            "not replace human judgment."
        )


# ─────────────────────────────────────────────────────────────────────────────
# INPUT FORM  — collects all 44 features from the user
# ─────────────────────────────────────────────────────────────────────────────
def render_input_form() -> dict:
    """
    Render the Streamlit input widgets and return a dict of raw user values.
    Categorical choices are kept as strings; encoding happens in preprocess_input().
    """
    raw = {}

    # ── Section 1: Personal & Demographic ───────────────────────────────────
    st.markdown('<div class="section-card"><h4>👤 Personal & Demographic</h4>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        raw["Age"]    = st.number_input("Age", min_value=18, max_value=65, value=35)
        raw["Gender"] = st.selectbox("Gender", ["Male", "Female"])
    with c2:
        raw["MaritalStatus"]   = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
        raw["DistanceFromHome"] = st.slider("Distance From Home (km)", 1, 30, 5)
    with c3:
        raw["Education"] = st.selectbox(
            "Education Level",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: {1:"Below College", 2:"College", 3:"Bachelor",
                                    4:"Master", 5:"Doctor"}[x],
            index=2,
        )
        raw["EducationField"] = st.selectbox(
            "Education Field",
            ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"],
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 2: Job Details ───────────────────────────────────────────────
    st.markdown('<div class="section-card"><h4>💼 Job Details</h4>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        raw["Department"] = st.selectbox(
            "Department", ["Sales", "Research & Development", "Human Resources"]
        )
        raw["JobRole"] = st.selectbox(
            "Job Role",
            ["Sales Executive", "Research Scientist", "Laboratory Technician",
             "Manufacturing Director", "Healthcare Representative", "Manager",
             "Sales Representative", "Research Director", "Human Resources"],
        )
        raw["JobLevel"] = st.selectbox(
            "Job Level", options=[1, 2, 3, 4, 5],
            format_func=lambda x: f"Level {x}",
        )
    with c2:
        raw["BusinessTravel"] = st.selectbox(
            "Business Travel", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"]
        )
        raw["OverTime"] = st.selectbox("OverTime", ["No", "Yes"])
        raw["JobInvolvement"] = st.selectbox(
            "Job Involvement",
            options=[1, 2, 3, 4],
            format_func=lambda x: {1:"Low", 2:"Medium", 3:"High", 4:"Very High"}[x],
            index=2,
        )
    with c3:
        raw["JobSatisfaction"] = st.selectbox(
            "Job Satisfaction",
            options=[1, 2, 3, 4],
            format_func=lambda x: {1:"Low", 2:"Medium", 3:"High", 4:"Very High"}[x],
            index=2,
        )
        raw["EnvironmentSatisfaction"] = st.selectbox(
            "Environment Satisfaction",
            options=[1, 2, 3, 4],
            format_func=lambda x: {1:"Low", 2:"Medium", 3:"High", 4:"Very High"}[x],
            index=2,
        )
        raw["WorkLifeBalance"] = st.selectbox(
            "Work-Life Balance",
            options=[1, 2, 3, 4],
            format_func=lambda x: {1:"Bad", 2:"Good", 3:"Better", 4:"Best"}[x],
            index=2,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 3: Compensation ──────────────────────────────────────────────
    st.markdown('<div class="section-card"><h4>💰 Compensation</h4>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        raw["MonthlyIncome"]    = st.number_input("Monthly Income ($)", 1_009, 19_999, 5_000, step=100)
        raw["DailyRate"]        = st.number_input("Daily Rate ($)", 102, 1_499, 800, step=10)
    with c2:
        raw["HourlyRate"]       = st.number_input("Hourly Rate ($)", 30, 100, 65)
        raw["MonthlyRate"]      = st.number_input("Monthly Rate ($)", 2_094, 26_999, 14_000, step=100)
    with c3:
        raw["PercentSalaryHike"] = st.slider("Percent Salary Hike (%)", 11, 25, 15)
        raw["StockOptionLevel"]  = st.selectbox(
            "Stock Option Level", options=[0, 1, 2, 3],
            format_func=lambda x: f"Level {x}",
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 4: Experience & Tenure ──────────────────────────────────────
    st.markdown('<div class="section-card"><h4>📅 Experience & Tenure</h4>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        raw["TotalWorkingYears"]     = st.slider("Total Working Years", 0, 40, 10)
        raw["NumCompaniesWorked"]    = st.slider("No. of Companies Worked", 0, 9, 2)
    with c2:
        raw["YearsAtCompany"]        = st.slider("Years At Company", 0, 40, 5)
        raw["YearsInCurrentRole"]    = st.slider("Years In Current Role", 0, 18, 3)
    with c3:
        raw["YearsSinceLastPromotion"] = st.slider("Years Since Last Promotion", 0, 15, 2)
        raw["YearsWithCurrManager"]    = st.slider("Years With Current Manager", 0, 17, 4)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 5: Development & Performance ────────────────────────────────
    st.markdown('<div class="section-card"><h4>📈 Development & Performance</h4>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        raw["TrainingTimesLastYear"] = st.slider("Training Times Last Year", 0, 6, 2)
    with c2:
        raw["PerformanceRating"] = st.selectbox(
            "Performance Rating",
            options=[3, 4],
            format_func=lambda x: {3:"Excellent", 4:"Outstanding"}[x],
        )
    with c3:
        raw["RelationshipSatisfaction"] = st.selectbox(
            "Relationship Satisfaction",
            options=[1, 2, 3, 4],
            format_func=lambda x: {1:"Low", 2:"Medium", 3:"High", 4:"Very High"}[x],
            index=2,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    return raw


# ─────────────────────────────────────────────────────────────────────────────
# RESULT DISPLAY
# ─────────────────────────────────────────────────────────────────────────────
def render_result(prediction: int, decision_score: float):
    """Display prediction result with confidence information."""
    st.markdown("---")
    st.subheader("🔮 Prediction Result")

    col_res, col_conf = st.columns([2, 1])

    with col_res:
        if prediction == 1:
            st.error(
                "⚠️  **This employee is likely to LEAVE the organisation.**\n\n"
                "Consider reviewing compensation, growth opportunities, or workload.",
                icon="🚪",
            )
        else:
            st.success(
                "✅  **This employee is likely to STAY with the organisation.**\n\n"
                "Continue nurturing their engagement and career development.",
                icon="🏢",
            )

    with col_conf:
        # decision_function() returns the signed distance from the hyperplane.
        # Positive → model predicts class 1 (Leave); Negative → class 0 (Stay).
        # We normalise with a sigmoid for display purposes.
        sigmoid_conf = 1 / (1 + np.exp(-decision_score))
        conf_pct     = sigmoid_conf * 100 if prediction == 1 else (1 - sigmoid_conf) * 100

        if conf_pct >= 70:
            badge_cls = "conf-high"
            label     = "High"
        elif conf_pct >= 45:
            badge_cls = "conf-medium"
            label     = "Moderate"
        else:
            badge_cls = "conf-low"
            label     = "Low"

        st.markdown(
            f"""
            <div style="text-align:center; padding:1rem;">
                <p style="margin:0; font-size:.9rem; opacity:.7;">Model Confidence</p>
                <p style="margin:.4rem 0; font-size:2.4rem; font-weight:700;">
                    {conf_pct:.1f}%
                </p>
                <span class="conf-badge {badge_cls}">{label} Confidence</span>
                <p style="margin:.8rem 0 0 0; font-size:.75rem; opacity:.6;">
                    Based on SVM decision function score: {decision_score:.4f}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Expandable technical detail
    with st.expander("ℹ️  About the confidence score"):
        st.markdown(
            """
            This SVM model was trained **without** `probability=True`, so
            `predict_proba()` is unavailable.  
            Instead, the **decision function** value (signed distance from the
            separating hyperplane) is passed through a sigmoid to produce an
            approximate probability.  

            | Score range | Interpretation |
            |---|---|
            | > +1 | Strongly predicts *Leave* |
            | 0 to +1 | Weakly predicts *Leave* |
            | -1 to 0 | Weakly predicts *Stay* |
            | < -1 | Strongly predicts *Stay* |

            To obtain calibrated probabilities, retrain with
            `SVC(probability=True)`.
            """
        )


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    inject_css()
    render_sidebar()

    # ── Hero banner ──────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero-banner">
            <h1>👥 Employee Attrition Prediction</h1>
            <p>
                HR Analytics System &nbsp;|&nbsp; Powered by Support Vector Machine (SVM)
                &nbsp;|&nbsp; Fill in the employee profile below and click <strong>Predict</strong>
                to assess attrition risk.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Input form ───────────────────────────────────────────────────────────
    raw_inputs = render_input_form()

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🔍  Predict Attrition Risk", type="primary", use_container_width=True)

    # ── Prediction pipeline ──────────────────────────────────────────────────
    if predict_btn:
        try:
            model, scaler = load_model()
        except FileNotFoundError as exc:
            st.error(
                f"❌  Model file not found: `{exc.filename}`\n\n"
                "Ensure both `.pkl` files are in the `models/` directory."
            )
            st.stop()

        with st.spinner("Running inference…"):
            input_df      = preprocess_input(raw_inputs)
            pred, d_score = predict(model, scaler, input_df)

        render_result(pred, d_score)

        # Optional: show the encoded feature vector for transparency
        with st.expander("🔬  Encoded Feature Vector (debug view)"):
            st.dataframe(input_df, use_container_width=True)


if __name__ == "__main__":
    main()