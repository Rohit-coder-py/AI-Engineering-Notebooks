"""
Fraud Sentinel — Credit Card Fraud Detection
A single-file Streamlit app. Run with:  streamlit run app.py
"""

import json
import os

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import torch
import torch.nn as nn

# ==============================================================================
# PATHS  (relative to this file, so it works locally AND on Streamlit Cloud)
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# ==============================================================================
# PAGE CONFIG + THEME
# ==============================================================================
st.set_page_config(
    page_title="Fraud Sentinel — Credit Card Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

:root {
    --bg-base:#0A0E14; --bg-panel:#131824; --bg-raised:#1A2130;
    --line:rgba(201,162,39,0.18); --line-soft:rgba(237,234,224,0.08);
    --gold:#C9A227; --gold-bright:#E4C55E;
    --emerald:#1E8A6E; --emerald-bright:#2FBF89;
    --oxblood:#7A1F2B; --oxblood-bright:#D1495B;
    --text-hi:#F3F0E6; --text-mid:#C8C3B8; --text-low:#8A8F9C;
}

.stApp {
    background:
        radial-gradient(ellipse 900px 500px at 8% -5%, rgba(201,162,39,0.10), transparent 60%),
        radial-gradient(ellipse 900px 600px at 95% 10%, rgba(30,138,110,0.10), transparent 55%),
        radial-gradient(ellipse 1200px 800px at 50% 110%, rgba(122,31,43,0.10), transparent 60%),
        var(--bg-base);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-panel) 0%, var(--bg-base) 100%) !important;
    border-right: 1px solid var(--line) !important;
}
[data-testid="stSidebar"] * { color: var(--text-mid) !important; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: var(--bg-raised); border: 1px solid var(--line-soft);
    border-radius: 8px; padding: 10px 14px !important; margin-bottom: 6px;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover { border-color: var(--gold); }

h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; color: var(--text-hi) !important; font-weight: 700 !important; }

.eyebrow { font-family:'JetBrains Mono',monospace; font-size:.72rem; letter-spacing:.18em;
    text-transform:uppercase; color:var(--gold); margin-bottom:.3rem; }

.stButton>button, .stDownloadButton>button {
    background: linear-gradient(180deg, var(--bg-raised), var(--bg-panel)) !important;
    color: var(--gold-bright) !important; border: 1px solid var(--gold) !important;
    border-radius: 8px !important; font-family:'JetBrains Mono',monospace !important;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    box-shadow: 0 0 16px rgba(201,162,39,.35) !important; color: var(--bg-base) !important;
    background: var(--gold-bright) !important;
}
.stButton>button[kind="primary"] {
    background: linear-gradient(135deg, var(--gold), var(--gold-bright)) !important;
    color: var(--bg-base) !important; font-weight: 700 !important;
}

.hero-wrap { border:1px solid var(--line); border-radius:16px;
    background: linear-gradient(155deg, var(--bg-panel) 0%, var(--bg-base) 100%);
    padding: 2.4rem 2.2rem 1.4rem 2.2rem; margin-bottom: 1.4rem; }
.hero-title { font-family:'Cormorant Garamond',serif; font-size:3rem; font-weight:700; line-height:1.05;
    background: linear-gradient(100deg, var(--gold-bright), var(--text-hi) 55%, var(--emerald-bright));
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { color: var(--text-mid); font-size: 1.02rem; max-width: 640px; line-height: 1.55; margin: .6rem 0 1rem 0; }

.ticker-outer { border-top:1px solid var(--line-soft); border-bottom:1px solid var(--line-soft);
    padding: 8px 0; overflow: hidden; white-space: nowrap; }
.ticker-track { display:inline-block; font-family:'JetBrains Mono',monospace; font-size:.82rem;
    color: var(--text-low); animation: scroll 38s linear infinite; }
.ticker-track span.ok { color: var(--emerald-bright); }
.ticker-track span.flag { color: var(--oxblood-bright); }
@keyframes scroll { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }
@media (prefers-reduced-motion: reduce) { .ticker-track { animation: none; } }

.card-row { display:flex; gap:14px; flex-wrap:wrap; margin-bottom:1.1rem; }
.metric-card { flex:1 1 180px; background:var(--bg-panel); border:1px solid var(--line-soft);
    border-left:3px solid var(--gold); border-radius:10px; padding:15px 18px; }
.metric-card.emerald { border-left-color: var(--emerald); }
.metric-card.oxblood { border-left-color: var(--oxblood); }
.m-label { font-family:'JetBrains Mono',monospace; font-size:.66rem; letter-spacing:.12em;
    text-transform:uppercase; color:var(--text-low); margin-bottom:6px; }
.m-value { font-family:'JetBrains Mono',monospace; font-size:1.6rem; font-weight:700; color:var(--text-hi); }
.m-sub { font-size:.76rem; color:var(--text-low); margin-top:4px; }

.panel { background:var(--bg-panel); border:1px solid var(--line-soft); border-radius:12px;
    padding:1.3rem 1.5rem; margin-bottom:1.1rem; }
.panel h4 { margin-top:0 !important; }

.seal-wrap { display:flex; align-items:center; gap:24px; flex-wrap:wrap; }
.seal { width:120px; height:120px; border-radius:50%; display:flex; align-items:center;
    justify-content:center; flex-direction:column; font-family:'JetBrains Mono',monospace; flex-shrink:0; }
.seal.safe { background: radial-gradient(circle at 35% 30%, rgba(47,191,137,.18), var(--bg-panel) 70%);
    border:2px solid var(--emerald-bright); box-shadow: 0 0 24px rgba(47,191,137,.35); }
.seal.flag { background: radial-gradient(circle at 35% 30%, rgba(209,73,91,.2), var(--bg-panel) 70%);
    border:2px solid var(--oxblood-bright); box-shadow: 0 0 24px rgba(209,73,91,.4);
    animation: pulse 1.8s ease-in-out infinite; }
@keyframes pulse { 0%,100%{box-shadow:0 0 20px rgba(209,73,91,.35)} 50%{box-shadow:0 0 32px rgba(209,73,91,.6)} }
.seal-pct { font-size:1.45rem; font-weight:700; }
.seal-tag { font-size:.58rem; letter-spacing:.1em; text-transform:uppercase; margin-top:2px; }
.seal.safe .seal-pct, .seal.safe .seal-tag { color: var(--emerald-bright); }
.seal.flag .seal-pct, .seal.flag .seal-tag { color: var(--oxblood-bright); }
.verdict-title { font-family:'Cormorant Garamond',serif; font-size:1.8rem; font-weight:700; margin-bottom:2px; }
.verdict-title.safe { color: var(--emerald-bright); }
.verdict-title.flag { color: var(--oxblood-bright); }
.verdict-desc { color: var(--text-mid); font-size:.9rem; max-width:440px; }

.pill { display:inline-block; font-family:'JetBrains Mono',monospace; font-size:.68rem; padding:3px 10px;
    border-radius:999px; border:1px solid var(--line); color:var(--gold-bright); background:rgba(201,162,39,.08); }
.gold-rule { border:none; height:1px; background: linear-gradient(90deg, transparent, var(--gold), transparent); margin: 1.4rem 0; }

.stTabs [data-baseweb="tab"] { background:var(--bg-panel); border:1px solid var(--line-soft);
    border-radius:8px 8px 0 0; color:var(--text-mid); font-family:'JetBrains Mono',monospace; font-size:.82rem; }
.stTabs [aria-selected="true"] { color: var(--gold-bright) !important; border-color: var(--gold) !important; }

[data-testid="stDataFrame"] { border:1px solid var(--line-soft); border-radius:8px; overflow:hidden; }

.footer-note { text-align:center; color:var(--text-low); font-family:'JetBrains Mono',monospace;
    font-size:.7rem; letter-spacing:.05em; margin-top:2.2rem; padding-top:1.1rem; border-top:1px solid var(--line-soft); }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# TINY HTML HELPERS
# ==============================================================================
def metric_card(label, value, sub="", accent="gold"):
    cls = "" if accent == "gold" else accent
    return f'<div class="metric-card {cls}"><div class="m-label">{label}</div><div class="m-value">{value}</div><div class="m-sub">{sub}</div></div>'


def card_row(*cards):
    return f'<div class="card-row">{"".join(cards)}</div>'


def panel(title, body_html):
    heading = f"<h4>{title}</h4>" if title else ""
    return f'<div class="panel">{heading}{body_html}</div>'


def pill(text):
    return f'<span class="pill">{text}</span>'


def verdict_seal(probability, threshold):
    is_fraud = probability >= threshold
    pct = f"{probability*100:.1f}%"
    seal_cls, title_cls = ("flag", "flag") if is_fraud else ("safe", "safe")
    title = "Flagged as Suspicious" if is_fraud else "Cleared as Legitimate"
    desc = (
        f"Estimated <b>{pct}</b> probability of fraud — at or above the "
        f"<b>{threshold*100:.0f}%</b> threshold. Recommend manual review."
        if is_fraud else
        f"Estimated <b>{pct}</b> probability of fraud — below the "
        f"<b>{threshold*100:.0f}%</b> threshold. No action needed."
    )
    return f'''
    <div class="seal-wrap">
        <div class="seal {seal_cls}"><div class="seal-pct">{pct}</div><div class="seal-tag">Risk Score</div></div>
        <div><div class="verdict-title {title_cls}">{title}</div><div class="verdict-desc">{desc}</div></div>
    </div>'''


# ==============================================================================
# MODEL + PREPROCESSING  (mirrors the notebook exactly)
# ==============================================================================
class FraudDetectionModel(nn.Module):
    def __init__(self, n_features=11):
        super().__init__()
        self.fc1 = nn.Linear(n_features, 16)
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc3(x)


@st.cache_resource(show_spinner="Loading model…")
def load_artifacts():
    encoder = joblib.load(os.path.join(MODELS_DIR, "encoder.pkl"))
    scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
    cat_cols = joblib.load(os.path.join(MODELS_DIR, "categorical_columns.pkl"))
    feature_order = joblib.load(os.path.join(MODELS_DIR, "feature_order.pkl"))

    model = FraudDetectionModel(n_features=len(feature_order))
    model.load_state_dict(torch.load(os.path.join(MODELS_DIR, "fraud_model.pth"), map_location="cpu"))
    model.eval()

    return {"model": model, "encoder": encoder, "scaler": scaler,
            "cat_cols": cat_cols, "feature_order": feature_order}


def predict(df: pd.DataFrame, threshold: float = 0.5):
    art = load_artifacts()
    X = df[art["feature_order"]].copy()
    X[art["cat_cols"]] = art["encoder"].transform(X[art["cat_cols"]])
    X_scaled = art["scaler"].transform(X)
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    with torch.no_grad():
        probs = torch.sigmoid(art["model"](X_tensor).squeeze(-1)).numpy()
    preds = (probs >= threshold).astype(int)
    return probs, preds


# ==============================================================================
# CACHED DATA LOADERS
# ==============================================================================
@st.cache_data(show_spinner=False)
def load_metrics():
    with open(os.path.join(MODELS_DIR, "metrics.json")) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_city_lookup():
    return pd.read_json(os.path.join(MODELS_DIR, "city_lookup.json")).set_index("city").to_dict("index")


@st.cache_data(show_spinner=False)
def load_merchant_lookup():
    return pd.read_json(os.path.join(MODELS_DIR, "merchant_lookup.json")).set_index("merchant").to_dict("index")


@st.cache_data(show_spinner=False)
def load_job_list():
    with open(os.path.join(MODELS_DIR, "job_list.json")) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_categories():
    return sorted(["entertainment", "food_dining", "gas_transport", "grocery_net", "grocery_pos",
                   "health_fitness", "home", "kids_pets", "misc_net", "misc_pos", "personal_care",
                   "shopping_net", "shopping_pos", "travel"])


@st.cache_data(show_spinner=False)
def load_sample_transactions():
    return pd.read_csv(os.path.join(MODELS_DIR, "sample_transactions.csv"))


@st.cache_data(show_spinner=False)
def load_data_preview(n=2000):
    return pd.read_csv(os.path.join(DATA_DIR, "credit_card_frauds_cleaned.csv"), nrows=n)


def img(name):
    return os.path.join(IMAGES_DIR, name)


def build_ticker(sample_df, n=14):
    rows = []
    sub = sample_df.sample(min(n, len(sample_df)))
    for _, r in sub.iterrows():
        tag = '<span class="flag">FLAGGED</span>' if r["is_fraud"] == 1 else '<span class="ok">CLEARED</span>'
        rows.append(f'{r["category"]} · ${r["amt"]:.2f} · {r["state"]} · {tag}')
    items = " &nbsp;•&nbsp; ".join(rows)
    return f'<div class="ticker-outer"><div class="ticker-track">{items} &nbsp;•&nbsp; {items}</div></div>'


# ==============================================================================
# SIDEBAR NAV
# ==============================================================================
with st.sidebar:
    st.markdown(
        "<div style='font-family:Cormorant Garamond,serif;font-size:1.6rem;font-weight:700;color:#E4C55E;'>🛡️ Fraud Sentinel</div>"
        "<div style='font-family:JetBrains Mono,monospace;font-size:.66rem;letter-spacing:.1em;color:#8A8F9C;margin-bottom:1.1rem;'>CREDIT CARD FRAUD DETECTION</div>",
        unsafe_allow_html=True,
    )
    page = st.radio("Navigate", ["Overview", "Predict", "Analytics", "Model Performance", "About"], label_visibility="collapsed")
    st.markdown("<div class='gold-rule'></div>", unsafe_allow_html=True)
    m = load_metrics()
    st.markdown(
        f"<div style='font-family:JetBrains Mono,monospace;font-size:.72rem;color:#8A8F9C;'>MODEL STATUS<br>"
        f"<span style='color:#2FBF89;'>● live</span> &nbsp;|&nbsp; ROC-AUC {m['roc_auc']:.3f}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='font-family:JetBrains Mono,monospace;font-size:.66rem;color:#5b5f6a;margin-top:2rem;'>Portfolio project · not for production use</div>",
        unsafe_allow_html=True,
    )

if st.session_state.get("_nav_hint"):
    page = st.session_state.pop("_nav_hint")


# ==============================================================================
# PAGE: OVERVIEW
# ==============================================================================
if page == "Overview":
    metrics = load_metrics()
    ticker_html = build_ticker(load_sample_transactions())

    st.markdown(f'''
    <div class="hero-wrap">
        <div class="eyebrow">Credit Card Fraud Detection · PyTorch ANN</div>
        <div class="hero-title">Fraud Sentinel</div>
        <div class="hero-sub">A neural network that screens credit-card transactions for fraud —
        trained on 339,607 real transactions across 14 merchant categories and 13 states,
        with a 189-to-1 legitimate-to-fraud imbalance.</div>
        {ticker_html}
    </div>''', unsafe_allow_html=True)

    st.markdown(card_row(
        metric_card("Transactions Analyzed", "339,607", "train + val + test"),
        metric_card("Fraud Rate", "0.52%", "1,782 confirmed fraud cases", "oxblood"),
        metric_card("Model Accuracy", f"{metrics['accuracy']*100:.2f}%", "held-out test set", "emerald"),
        metric_card("ROC-AUC", f"{metrics['roc_auc']:.3f}", "risk-ranking quality", "emerald"),
    ), unsafe_allow_html=True)

    c1, c2 = st.columns([1.3, 1])
    with c1:
        st.markdown(panel("How it works",
            "<p style='color:#C8C3B8;line-height:1.6;'>Every transaction is described by 11 features — "
            "merchant, category, amount, cardholder location/job, and merchant location. A compact network "
            f"({pill('11 → 16 → 8 → 1')}) scores each transaction's fraud probability; you set the decision "
            "threshold.</p>"
            f"<p style='color:#8A8F9C;font-size:.85rem;'>Fraud is only 0.52% of transactions, so the model is "
            f"tuned to rank risk well (ROC-AUC {metrics['roc_auc']:.3f}) even though recall at the default "
            "threshold is modest — see <b>Model Performance</b> for the honest breakdown.</p>"
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(panel("Try it now",
            "<p style='color:#C8C3B8;'>Head to <b>Predict</b> to score a transaction, load a real sample, "
            "or upload a batch CSV.</p>"
        ), unsafe_allow_html=True)
        if st.button("Go to Predict →", width="stretch", type="primary"):
            st.session_state["_nav_hint"] = "Predict"
            st.rerun()

    st.markdown("<div class='gold-rule'></div>", unsafe_allow_html=True)
    st.markdown("#### Dataset snapshot")
    st.dataframe(load_data_preview().head(8), width="stretch", hide_index=True)


# ==============================================================================
# PAGE: PREDICT
# ==============================================================================
elif page == "Predict":
    st.markdown("<div class='eyebrow'>Score a transaction</div><h1 style='margin-top:0;'>Predict</h1>", unsafe_allow_html=True)

    city_lookup = load_city_lookup()
    merchant_lookup = load_merchant_lookup()
    job_list = load_job_list()
    categories = load_categories()
    cities = sorted(city_lookup.keys())
    merchants = sorted(merchant_lookup.keys())

    tab_single, tab_batch = st.tabs(["🔎 Single transaction", "📁 Batch upload"])

    with tab_single:
        left, right = st.columns([1, 1.15])
        if "form_defaults" not in st.session_state:
            st.session_state.form_defaults = None

        with left:
            st.markdown('<div class="panel"><h4>Transaction details</h4>', unsafe_allow_html=True)
            if st.button("🎲 Load a random real transaction", width="stretch"):
                st.session_state.form_defaults = load_sample_transactions().sample(1).iloc[0].to_dict()
                st.rerun()

            d = st.session_state.form_defaults or {}
            category = st.selectbox("Merchant category", categories,
                                     index=categories.index(d["category"]) if d.get("category") in categories else 0)
            amt = st.number_input("Transaction amount ($)", min_value=0.01, max_value=50000.0,
                                   value=float(d.get("amt", 45.0)), step=1.0)
            merchant = st.selectbox("Merchant", merchants,
                                     index=merchants.index(d["merchant"]) if d.get("merchant") in merchants else 0)
            city = st.selectbox("Cardholder city", cities,
                                 index=cities.index(d["city"]) if d.get("city") in cities else 0)
            city_info = city_lookup[city]
            job_default = d.get("job", job_list[0])
            job = st.selectbox("Cardholder occupation", job_list,
                                index=job_list.index(job_default) if job_default in job_list else 0)

            with st.expander("Advanced — geolocation (auto-filled from city / merchant)"):
                state = st.text_input("State", value=city_info["state"], disabled=True)
                lat = st.number_input("Cardholder latitude", value=float(city_info["lat"]))
                long = st.number_input("Cardholder longitude", value=float(city_info["long"]))
                city_pop = st.number_input("City population", min_value=1, value=int(city_info["city_pop"]))
                m_info = merchant_lookup[merchant]
                merch_lat = st.number_input("Merchant latitude", value=float(m_info["merch_lat"]))
                merch_long = st.number_input("Merchant longitude", value=float(m_info["merch_long"]))

            threshold = st.slider("Decision threshold", 0.05, 0.95, 0.50, 0.05,
                                   help="Lower this to catch more fraud at the cost of more false alarms.")
            go = st.button("🛡️ Score this transaction", type="primary", width="stretch")
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            if go:
                row = pd.DataFrame([{
                    "merchant": merchant, "category": category, "amt": amt, "city": city, "state": state,
                    "lat": lat, "long": long, "city_pop": city_pop, "job": job,
                    "merch_lat": merch_lat, "merch_long": merch_long,
                }])
                probs, preds = predict(row, threshold=threshold)
                prob = float(probs[0])

                st.markdown(panel("Verdict", verdict_seal(prob, threshold)), unsafe_allow_html=True)
                st.progress(min(max(prob, 0.0), 1.0), text=f"Fraud probability — {prob*100:.1f}%")

                if st.session_state.get("form_defaults") and "is_fraud" in st.session_state.form_defaults:
                    actual = "Fraud" if st.session_state.form_defaults["is_fraud"] == 1 else "Legitimate"
                    st.caption(f"Ground truth for this loaded sample: **{actual}**")

                with st.expander("Raw feature values sent to the model"):
                    display_row = row.T.rename(columns={0: "value"})
                    display_row["value"] = display_row["value"].astype(str)
                    st.dataframe(display_row, width="stretch")
            else:
                st.markdown(panel("Verdict",
                    "<p style='color:#8A8F9C;'>Fill in the transaction details and click "
                    "<b>Score this transaction</b> to see the fraud probability here.</p>"
                ), unsafe_allow_html=True)

    with tab_batch:
        st.markdown(panel("Batch scoring",
            "<p style='color:#C8C3B8;'>Upload a CSV with columns: "
            f"{pill('merchant, category, amt, city, state, lat, long, city_pop, job, merch_lat, merch_long')}</p>"
        ), unsafe_allow_html=True)
        batch_threshold = st.slider("Batch decision threshold", 0.05, 0.95, 0.50, 0.05, key="batch_thresh")
        uploaded = st.file_uploader("Upload transactions CSV", type=["csv"])
        use_sample = st.button("Or try it with the bundled sample transactions")

        df_in = None
        if uploaded is not None:
            df_in = pd.read_csv(uploaded)
        elif use_sample:
            df_in = load_sample_transactions().drop(columns=["is_fraud"], errors="ignore")

        if df_in is not None:
            try:
                probs, preds = predict(df_in, threshold=batch_threshold)
                out = df_in.copy()
                out["fraud_probability"] = probs
                out["prediction"] = np.where(preds == 1, "Fraud", "Legitimate")
                n_flagged = int(preds.sum())
                st.markdown(card_row(
                    metric_card("Rows Scored", f"{len(out):,}"),
                    metric_card("Flagged as Fraud", f"{n_flagged:,}", accent="oxblood"),
                    metric_card("Flag Rate", f"{n_flagged/len(out)*100:.2f}%", accent="oxblood"),
                ), unsafe_allow_html=True)
                st.dataframe(out, width="stretch", hide_index=True)
                st.download_button("⬇ Download scored CSV", out.to_csv(index=False).encode(),
                                    file_name="scored_transactions.csv", mime="text/csv")
            except Exception as e:
                st.error(f"Couldn't score this file — check the column names match. ({e})")


# ==============================================================================
# PAGE: ANALYTICS
# ==============================================================================
elif page == "Analytics":
    st.markdown("<div class='eyebrow'>Exploratory data analysis</div><h1 style='margin-top:0;'>Analytics</h1>", unsafe_allow_html=True)

    st.markdown(panel("Target distribution",
        "<p style='color:#8A8F9C;'>Fraud makes up only 0.52% of all transactions — the central "
        "challenge this model has to work around.</p>"
    ), unsafe_allow_html=True)
    st.image(img("01_target_distribution.png"), width="stretch")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Amount distribution")
        st.image(img("02_amount_distribution.png"), width="stretch")
        st.caption("Fraudulent transactions average ~$518 vs ~$68 for legitimate ones.")
    with c2:
        st.markdown("#### Correlation heatmap")
        st.image(img("05_correlation_heatmap.png"), width="stretch")
        st.caption("No single numeric feature is strongly linearly correlated with fraud in isolation.")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("#### Fraud rate by category")
        st.image(img("03_category_fraud_rate.png"), width="stretch")
    with c4:
        st.markdown("#### Fraud rate by state")
        st.image(img("04_state_fraud_rate.png"), width="stretch")

    st.markdown("<div class='gold-rule'></div>", unsafe_allow_html=True)
    st.markdown(panel("Key observations", """
        <ul style='color:#C8C3B8;line-height:1.8;'>
        <li><b style='color:#D1495B;'>Extreme class imbalance</b> — 1 fraud for every ~189 legitimate transactions.</li>
        <li><b style='color:#2FBF89;'>Amount is the strongest signal</b> — fraud transactions run ~7.6x higher on average.</li>
        <li><b style='color:#C9A227;'>Category matters</b> — online/card-not-present categories skew riskier.</li>
        <li><b>Geography has mild signal</b> — weaker than amount or category, but not negligible.</li>
        </ul>"""), unsafe_allow_html=True)


# ==============================================================================
# PAGE: MODEL PERFORMANCE
# ==============================================================================
elif page == "Model Performance":
    st.markdown("<div class='eyebrow'>Held-out test set — 50,942 transactions</div><h1 style='margin-top:0;'>Model Performance</h1>", unsafe_allow_html=True)

    metrics = load_metrics()
    st.markdown(card_row(
        metric_card("Accuracy", f"{metrics['accuracy']*100:.2f}%", "misleading alone — see note below"),
        metric_card("Fraud Precision", f"{metrics['precision']*100:.1f}%", "of flags that are real fraud", "emerald"),
        metric_card("Fraud Recall", f"{metrics['recall']*100:.1f}%", "of fraud actually caught", "oxblood"),
        metric_card("ROC-AUC", f"{metrics['roc_auc']:.3f}", "risk-ranking quality", "emerald"),
    ), unsafe_allow_html=True)

    st.markdown(panel("⚠ Reading these numbers honestly",
        "<p style='color:#C8C3B8;line-height:1.6;'>With fraud at just 0.52% of transactions, a model that "
        "predicts \"legitimate\" for everything would already score ~99.5% accuracy while catching zero fraud. "
        "<b>Recall (32.8%)</b> is the real bottleneck — at the default 0.5 threshold the model catches about "
        "1 in 3 fraud cases, because it was trained with a plain loss function (no class weighting) against a "
        "~189:1 imbalance. ROC-AUC of 0.91 shows the underlying risk ranking is genuinely good — lowering the "
        "decision threshold (try it on the Predict page) trades some precision for meaningfully higher recall.</p>"
    ), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Confusion matrix")
        st.image(img("06_confusion_matrix.png"), width="stretch")
    with c2:
        st.markdown("#### ROC curve")
        st.image(img("07_roc_curve.png"), width="stretch")

    st.markdown("<div class='gold-rule'></div>", unsafe_allow_html=True)
    st.markdown("#### Classification report")
    st.dataframe(pd.DataFrame({
        "class": ["Legitimate", "Fraud"],
        "precision": [0.9965, metrics["precision"]],
        "recall": [0.9994, metrics["recall"]],
        "f1-score": [0.9979, metrics["f1_score"]],
        "support": [50674, metrics["fraud_in_test"]],
    }), width="stretch", hide_index=True)


# ==============================================================================
# PAGE: ABOUT
# ==============================================================================
elif page == "About":
    st.markdown("<div class='eyebrow'>Project details</div><h1 style='margin-top:0;'>About</h1>", unsafe_allow_html=True)

    st.markdown(panel("Business problem",
        "<p style='color:#C8C3B8;line-height:1.6;'>Card issuers need to flag fraudulent transactions fast "
        "enough to block them, without drowning legitimate cardholders in false declines. This project builds "
        "a screening model over 339,607 real transactions to explore that trade-off.</p>"
    ), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(panel("Model architecture", """
            <table style='width:100%;color:#C8C3B8;font-family:JetBrains Mono,monospace;font-size:.85rem;'>
            <tr><td>Input features</td><td>11</td></tr>
            <tr><td>Hidden layer 1</td><td>16 units, ReLU</td></tr>
            <tr><td>Hidden layer 2</td><td>8 units, ReLU</td></tr>
            <tr><td>Output</td><td>1 logit (sigmoid)</td></tr>
            <tr><td>Loss</td><td>BCEWithLogitsLoss</td></tr>
            <tr><td>Optimizer</td><td>Adam, lr=1e-3</td></tr>
            <tr><td>Epochs</td><td>10</td></tr>
            </table>"""), unsafe_allow_html=True)
    with c2:
        st.markdown(panel("Features used",
            "<p style='color:#C8C3B8;font-size:.9rem;line-height:1.7;'>merchant · category · amt · city · "
            "state · lat · long · city_pop · job · merch_lat · merch_long</p>"
            "<p style='color:#8A8F9C;font-size:.82rem;'>Dropped as identifiers/leakage: trans_date_trans_time, dob, trans_num.</p>"
        ), unsafe_allow_html=True)

    st.markdown(panel("Tech stack",
        "<div>" + " ".join(pill(x) for x in
            ["PyTorch", "scikit-learn", "pandas", "Streamlit", "OrdinalEncoder", "StandardScaler"]) + "</div>"
    ), unsafe_allow_html=True)

    st.markdown(panel("Disclaimer",
        "<p style='color:#8A8F9C;font-size:.85rem;'>This model is a data-science portfolio project, not a "
        "certified fraud-detection system. Do not use it to make real financial or legal decisions.</p>"
    ), unsafe_allow_html=True)

    st.markdown('<div class="footer-note">FRAUD SENTINEL · BUILT WITH PYTORCH + STREAMLIT</div>', unsafe_allow_html=True)
