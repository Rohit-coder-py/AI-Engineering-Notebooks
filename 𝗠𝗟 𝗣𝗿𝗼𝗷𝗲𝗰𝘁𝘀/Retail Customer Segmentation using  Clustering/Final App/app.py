"""
Retail Customer Segmentation — Streamlit App
---------------------------------------------
Loads a pre-trained K-Means model + StandardScaler and predicts which
customer segment a shopper belongs to, based on Age, Annual Income and
Spending Score. Styled as a quiet, boutique-grade analytics tool.
"""

import pickle
import random
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# MODEL PATHS
# ============================================================
KMEANS_PRIMARY_PATH = r"C:\Users\shobh\Downloads\AI and DATA SCIENCE\𝗠𝗟 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀\Retail Customer Segmentation using  Clustering\models\kmeans_model.pkl"
SCALER_PRIMARY_PATH = r"C:\Users\shobh\Downloads\AI and DATA SCIENCE\𝗠𝗟 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀\Retail Customer Segmentation using  Clustering\models\scaler.pkl"

KMEANS_FALLBACK_PATH = Path(__file__).parent / "models" / "kmeans_model.pkl"
SCALER_FALLBACK_PATH = Path(__file__).parent / "models" / "scaler.pkl"

FEATURE_ORDER = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]

# ============================================================
# CLUSTER INFORMATION — jewel-tone palette, each tied to segment meaning
# ============================================================
CLUSTER_INFO = {
    0: {
        "name": "Senior Value Customers",
        "short": "Value & Loyalty",
        "description": "Older customers with moderate income and relatively low spending.",
        "color": "#B9793C",   # copper
        "recommendations": [
            "Senior citizen offers",
            "Loyalty rewards",
            "Festival discounts",
            "Value-based promotions",
        ],
    },
    1: {
        "name": "Premium Customers",
        "short": "Highest Value",
        "description": "High income and high spending customers — the most valuable segment.",
        "color": "#C9A24B",   # brass gold
        "recommendations": [
            "VIP membership",
            "Premium services",
            "Exclusive rewards",
            "Early access offers",
        ],
    },
    2: {
        "name": "Young Active Shoppers",
        "short": "Growth Segment",
        "description": "Young customers with moderate income and good spending habits.",
        "color": "#3F7859",   # emerald
        "recommendations": [
            "Student offers",
            "Flash sales",
            "Social media campaigns",
            "Reward points",
        ],
    },
    3: {
        "name": "Affluent Conservative Customers",
        "short": "Untapped Potential",
        "description": "High income but low spending — strong purchasing power left untapped.",
        "color": "#3E5C8A",   # sapphire
        "recommendations": [
            "Personalized recommendations",
            "Luxury promotions",
            "Premium memberships",
            "Targeted marketing campaigns",
        ],
    },
}

# ============================================================
# STYLING — boutique / atelier aesthetic
# ============================================================
def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Jost:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] { font-family: 'Jost', sans-serif; }

        .stApp {
            background:
                radial-gradient(ellipse 900px 500px at 12% -5%, rgba(201,162,75,0.07), transparent 60%),
                #100D0B;
            color: #EDE6D9;
        }

        section.main > div { padding-top: 1.4rem; }

        h1, h2, h3, h4 { font-family: 'Cormorant Garamond', serif; font-weight: 600; }

        /* ---------- Eyebrow / label system ---------- */
        .eyebrow {
            font-family: 'Jost', sans-serif;
            font-size: 0.72rem;
            letter-spacing: 0.28em;
            text-transform: uppercase;
            color: #C9A24B;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }

        /* ---------- Hero ---------- */
        .hero-title {
            font-family: 'Cormorant Garamond', serif;
            font-weight: 600;
            font-size: 3rem;
            letter-spacing: 0.01em;
            color: #F4EEE1;
            margin: 0 0 0.3rem 0;
            line-height: 1.1;
        }
        .hero-rule {
            width: 64px; height: 1px;
            background: linear-gradient(90deg, #C9A24B, transparent);
            margin: 0.9rem 0 1rem 0;
        }
        .hero-subtitle {
            color: #9C9284;
            font-size: 1rem;
            font-weight: 300;
            max-width: 640px;
            margin-bottom: 1.4rem;
        }

        /* ---------- Generic panel ---------- */
        .panel {
            background: #17130F;
            border: 1px solid rgba(201,162,75,0.16);
            border-top: 1px solid rgba(201,162,75,0.55);
            border-radius: 3px;
            padding: 1.5rem 1.7rem;
        }

        /* ---------- Section headers ---------- */
        .section-head {
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.35rem;
            font-weight: 600;
            color: #F4EEE1;
            margin: 0 0 1rem 0;
            letter-spacing: 0.01em;
        }

        /* ---------- Membership-style result card ---------- */
        .membership-card {
            position: relative;
            background: linear-gradient(180deg, #18140F 0%, #14110D 100%);
            border: 1px solid rgba(201,162,75,0.35);
            border-radius: 4px;
            padding: 2.2rem 2.4rem;
        }
        .membership-card::before, .membership-card::after {
            content: "";
            position: absolute; width: 22px; height: 22px;
            border-color: #C9A24B; border-style: solid; opacity: 0.75;
        }
        .membership-card::before {
            top: 10px; left: 10px;
            border-width: 1px 0 0 1px;
        }
        .membership-card::after {
            bottom: 10px; right: 10px;
            border-width: 0 1px 1px 0;
        }
        .mc-eyebrow {
            font-size: 0.7rem; letter-spacing: 0.3em; text-transform: uppercase;
            color: #9C9284; text-align: center; margin-bottom: 0.6rem;
        }
        .mc-name {
            font-family: 'Cormorant Garamond', serif;
            font-size: 2.1rem; font-weight: 700; text-align: center;
            margin: 0.1rem 0 0.7rem 0;
        }
        .mc-seal {
            text-align: center; color: #C9A24B; font-size: 0.85rem;
            letter-spacing: 0.35em; margin: 0.4rem 0 1rem 0; opacity: 0.85;
        }
        .mc-desc {
            text-align: center; color: #B7AC9B; font-style: italic;
            font-family: 'Cormorant Garamond', serif; font-size: 1.15rem;
            max-width: 520px; margin: 0 auto 1.5rem auto; line-height: 1.5;
        }
        .mc-rec-title {
            text-align: center; font-size: 0.68rem; letter-spacing: 0.28em;
            text-transform: uppercase; color: #9C9284; margin-bottom: 0.9rem;
        }
        .mc-rec-grid {
            display: flex; flex-wrap: wrap; justify-content: center; gap: 0.6rem 1rem;
        }
        .mc-rec-item {
            font-family: 'Jost', sans-serif; font-size: 0.88rem; color: #EDE6D9;
            border: 1px solid rgba(201,162,75,0.3);
            padding: 0.5rem 1.1rem; border-radius: 2px;
            background: rgba(201,162,75,0.045);
        }

        /* ---------- Metric boxes ---------- */
        .metric-box {
            border: 1px solid rgba(201,162,75,0.18);
            border-top: 1px solid rgba(201,162,75,0.5);
            padding: 1rem 1.2rem; text-align: center; border-radius: 3px;
            background: #14110D;
        }
        .metric-label {
            font-size: 0.66rem; letter-spacing: 0.24em; text-transform: uppercase;
            color: #9C9284; margin-bottom: 0.5rem;
        }
        .metric-value {
            font-family: 'JetBrains Mono', monospace; font-size: 1.5rem;
            color: #F4EEE1; font-weight: 500;
        }

        /* ---------- Analysis note ---------- */
        .analysis-note {
            color: #B7AC9B; font-size: 0.95rem; line-height: 1.65;
        }
        .analysis-note b { color: #EDE6D9; font-weight: 500; }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background: #0C0A08;
            border-right: 1px solid rgba(201,162,75,0.14);
        }
        section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }
        .side-eyebrow {
            font-size: 0.68rem; letter-spacing: 0.26em; text-transform: uppercase;
            color: #C9A24B; margin-bottom: 0.8rem;
        }
        .side-title {
            font-family: 'Cormorant Garamond', serif; font-size: 1.5rem;
            color: #F4EEE1; margin-bottom: 0.9rem;
        }
        .side-divider {
            width: 100%; height: 1px;
            background: rgba(201,162,75,0.2); margin: 1.1rem 0;
        }
        .side-fact { font-size: 0.86rem; color: #A79A88; line-height: 2; }
        .side-fact b { color: #D9CFBE; font-weight: 500; }
        .segment-row {
            display: flex; align-items: baseline; gap: 0.6rem; margin: 0.55rem 0;
        }
        .segment-dot {
            width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0;
            transform: translateY(-1px);
        }
        .segment-label {
            font-size: 0.86rem; color: #D9CFBE; font-weight: 400;
        }
        .segment-sub { font-size: 0.74rem; color: #83786A; margin-left: 1.15rem; }

        /* ---------- Inputs ---------- */
        div[data-testid="stNumberInput"] label {
            font-size: 0.7rem !important; letter-spacing: 0.18em; text-transform: uppercase;
            color: #9C9284 !important; font-weight: 500 !important;
        }
        div[data-testid="stNumberInput"] input {
            font-family: 'JetBrains Mono', monospace !important;
            background: #14110D !important;
            border: 1px solid rgba(201,162,75,0.25) !important;
            color: #F4EEE1 !important;
        }

        /* ---------- Buttons ---------- */
        .stButton > button {
            border-radius: 2px;
            font-family: 'Jost', sans-serif;
            font-size: 0.82rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            font-weight: 500;
            padding: 0.65rem 1rem;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(180deg, #D8B968, #B4903E);
            color: #14110D;
            border: none;
        }
        .stButton > button[kind="secondary"] {
            background: transparent;
            color: #EDE6D9;
            border: 1px solid rgba(201,162,75,0.4);
        }

        div[data-testid="stAlert"] {
            background: #17130F;
            border: 1px solid rgba(201,162,75,0.25);
            color: #D9CFBE;
        }

        hr { border-color: rgba(201,162,75,0.15) !important; }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-thumb { background: rgba(201,162,75,0.3); border-radius: 4px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# MODEL LOADING
# ============================================================
@st.cache_resource(show_spinner="Loading trained model...")
def load_models():
    kmeans_candidates = [Path(KMEANS_PRIMARY_PATH), KMEANS_FALLBACK_PATH]
    scaler_candidates = [Path(SCALER_PRIMARY_PATH), SCALER_FALLBACK_PATH]

    def _load_first_existing(candidates, label):
        for path in candidates:
            if path.exists():
                with open(path, "rb") as f:
                    return pickle.load(f), None
        return None, (
            f"Could not find the {label} file. Looked in:\n"
            + "\n".join(f"  • {p}" for p in candidates)
        )

    kmeans, kmeans_err = _load_first_existing(kmeans_candidates, "K-Means model")
    scaler, scaler_err = _load_first_existing(scaler_candidates, "Scaler")

    error = None
    if kmeans_err or scaler_err:
        error = "\n\n".join(filter(None, [kmeans_err, scaler_err]))

    return kmeans, scaler, error


# ============================================================
# PREDICTION HELPERS
# ============================================================
def predict_cluster(kmeans, scaler, age: float, income: float, spending: float) -> int:
    input_df = pd.DataFrame([[age, income, spending]], columns=FEATURE_ORDER)
    scaled = scaler.transform(input_df)
    return int(kmeans.predict(scaled)[0])


@st.cache_data(show_spinner=False)
def build_reference_data(_kmeans, _scaler, n_samples: int = 240, seed: int = 42) -> pd.DataFrame:
    """
    Builds a synthetic, illustrative customer dataset for the scatter plot by
    sampling around each cluster's centroid (in the model's own scaled space)
    and re-labelling every point with the real model. Keeps the plot visually
    informative without shipping the original training CSV with the app.
    """
    rng = np.random.default_rng(seed)
    centers = _kmeans.cluster_centers_
    n_clusters = centers.shape[0]
    per_cluster = max(1, n_samples // n_clusters)

    scaled_points = []
    for c in centers:
        noise = rng.normal(loc=0.0, scale=0.45, size=(per_cluster, len(c)))
        scaled_points.append(c + noise)
    scaled_points = np.vstack(scaled_points)

    raw_points = _scaler.inverse_transform(scaled_points)
    df = pd.DataFrame(raw_points, columns=FEATURE_ORDER)

    df["Age"] = df["Age"].clip(18, 80).round(0)
    df["Annual Income (k$)"] = df["Annual Income (k$)"].clip(10, 150).round(0)
    df["Spending Score (1-100)"] = df["Spending Score (1-100)"].clip(1, 100).round(0)

    df["Cluster"] = _kmeans.predict(_scaler.transform(df[FEATURE_ORDER]))
    return df


def random_customer() -> dict:
    return {
        "age": random.randint(18, 70),
        "income": random.randint(15, 140),
        "spending": random.randint(1, 100),
    }


# ============================================================
# UI SECTIONS
# ============================================================
def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="side-eyebrow">Project Dossier</div>', unsafe_allow_html=True)
        st.markdown('<div class="side-title">Customer<br>Segmentation</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="side-fact">
            <b>Method</b> — K-Means Clustering<br>
            <b>Segments</b> — 4<br>
            <b>Inputs</b> — Age, Income, Spending<br>
            <b>Preprocessing</b> — StandardScaler
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="side-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="side-eyebrow">The Four Segments</div>', unsafe_allow_html=True)

        for info in CLUSTER_INFO.values():
            st.markdown(
                f"""
                <div class="segment-row">
                    <span class="segment-dot" style="background:{info['color']};"></span>
                    <span class="segment-label">{info['name']}</span>
                </div>
                <div class="segment-sub">{info['short']}</div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown('<div class="side-divider"></div>', unsafe_allow_html=True)
        st.caption("Streamlit · scikit-learn")


def render_header():
    st.markdown('<div class="eyebrow">Retail Analytics · K-Means Clustering</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Customer Segmentation</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-rule"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Enter a customer\'s profile to identify their market '
        "segment and the strategy best suited to them, using a K-Means model trained on "
        "Age, Annual Income and Spending Score.</div>",
        unsafe_allow_html=True,
    )


def render_inputs():
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-head">Customer Profile</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input(
            "Age", min_value=18, max_value=100, value=st.session_state.get("age", 30), step=1
        )
    with c2:
        income = st.number_input(
            "Annual Income (k$)",
            min_value=0,
            max_value=300,
            value=st.session_state.get("income", 60),
            step=1,
        )
    with c3:
        spending = st.number_input(
            "Spending Score (1-100)",
            min_value=1,
            max_value=100,
            value=st.session_state.get("spending", 50),
            step=1,
        )

    st.session_state["age"] = age
    st.session_state["income"] = income
    st.session_state["spending"] = spending

    st.write("")
    b1, b2 = st.columns(2)
    with b1:
        predict_clicked = st.button("Predict Segment", type="primary", width='stretch')
    with b2:
        random_clicked = st.button("Random Customer", type="secondary", width='stretch')

    st.markdown("</div>", unsafe_allow_html=True)
    return age, income, spending, predict_clicked, random_clicked


def render_result_card(cluster_id: int):
    info = CLUSTER_INFO[cluster_id]
    items = "".join(f'<div class="mc-rec-item">{r}</div>' for r in info["recommendations"])
    st.markdown(
        f"""
        <div class="membership-card">
            <div class="mc-eyebrow">Segment {cluster_id} of 4</div>
            <div class="mc-name" style="color:{info['color']};">{info['name']}</div>
            <div class="mc-seal">✦ ✦ ✦</div>
            <div class="mc-desc">{info['description']}</div>
            <div class="mc-rec-title">Recommended Strategy</div>
            <div class="mc-rec-grid">{items}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_business_analysis(cluster_id: int, age: float, income: float, spending: float):
    info = CLUSTER_INFO[cluster_id]
    st.markdown('<div class="section-head">Business Analysis</div>', unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    for col, label, value in zip(
        (m1, m2, m3),
        ("Age", "Annual Income", "Spending Score"),
        (f"{int(age)}", f"${int(income)}k", f"{int(spending)} / 100"),
    ):
        col.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown(
        f"""
        <div class="panel">
        <p class="analysis-note">
        This customer falls into the <b style="color:{info['color']};">{info['name']}</b> segment —
        {info['description'][0].lower()}{info['description'][1:]}
        </p>
        <p class="analysis-note" style="margin-bottom:0;">
        Recommended focus: <b>{info['recommendations'][0]}</b> and
        <b>{info['recommendations'][1]}</b>, to strengthen engagement and long-term value
        within this segment.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_scatter_plot(df: pd.DataFrame, predicted_point: dict, predicted_cluster: int):
    st.markdown('<div class="section-head">Segment Landscape</div>', unsafe_allow_html=True)

    fig = go.Figure()

    for cid, info in CLUSTER_INFO.items():
        cluster_df = df[df["Cluster"] == cid]
        fig.add_trace(
            go.Scatter(
                x=cluster_df["Annual Income (k$)"],
                y=cluster_df["Spending Score (1-100)"],
                mode="markers",
                name=info["name"],
                marker=dict(size=8, color=info["color"], opacity=0.5, line=dict(width=0)),
                hovertemplate="Income: %{x}k<br>Spending: %{y}<extra>%{fullData.name}</extra>",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[predicted_point["income"]],
            y=[predicted_point["spending"]],
            mode="markers",
            name="Predicted Customer",
            marker=dict(
                size=17,
                color=CLUSTER_INFO[predicted_cluster]["color"],
                symbol="diamond",
                line=dict(width=1.5, color="#F4EEE1"),
            ),
            hovertemplate="Predicted Customer<br>Income: %{x}k<br>Spending: %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Jost, sans-serif", color="#D9CFBE", size=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", yanchor="bottom", y=1.02),
        xaxis_title="Annual Income (k$)",
        yaxis_title="Spending Score (1-100)",
        margin=dict(l=10, r=10, t=40, b=10),
        height=460,
    )
    fig.update_xaxes(gridcolor="rgba(201,162,75,0.12)", zeroline=False, tickfont=dict(family="JetBrains Mono"))
    fig.update_yaxes(gridcolor="rgba(201,162,75,0.12)", zeroline=False, tickfont=dict(family="JetBrains Mono"))

    st.plotly_chart(fig, width='stretch')
    st.caption(
        "Points are an illustrative distribution generated around each cluster's centroid "
        "and re-labelled by the trained model, since the original training dataset is not "
        "bundled with this app."
    )


# ============================================================
# MAIN APP
# ============================================================
def main():
    inject_css()

    kmeans, scaler, error = load_models()

    render_header()
    render_sidebar()

    if error:
        st.error(
            "Could not load the trained model files.\n\n"
            f"{error}\n\n"
            "Place `kmeans_model.pkl` and `scaler.pkl` in a `models/` folder "
            "next to `app.py`, or update the paths at the top of the script."
        )
        st.stop()

    if st.session_state.get("_trigger_random", False):
        rc = random_customer()
        st.session_state["age"] = rc["age"]
        st.session_state["income"] = rc["income"]
        st.session_state["spending"] = rc["spending"]
        st.session_state["_trigger_random"] = False

    age, income, spending, predict_clicked, random_clicked = render_inputs()

    if random_clicked:
        st.session_state["_trigger_random"] = True
        st.rerun()

    if predict_clicked:
        st.session_state["_has_prediction"] = True
        st.session_state["_last_input"] = {"age": age, "income": income, "spending": spending}

    st.write("")

    if st.session_state.get("_has_prediction"):
        last = st.session_state["_last_input"]
        try:
            cluster_id = predict_cluster(kmeans, scaler, last["age"], last["income"], last["spending"])
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            st.stop()

        render_result_card(cluster_id)
        st.write("")
        render_business_analysis(cluster_id, last["age"], last["income"], last["spending"])
        st.write("")

        reference_df = build_reference_data(kmeans, scaler)
        render_scatter_plot(reference_df, last, cluster_id)
    else:
        st.info("Enter a customer profile above and click **Predict Segment** to see results.")


if __name__ == "__main__":
    main()