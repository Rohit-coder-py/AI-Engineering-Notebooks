"""
Shipment Delay Intelligence
============================
A production-quality Streamlit application for predicting whether a
shipment will arrive on time or be delayed, built on top of a
StackingClassifier trained in `notebook/shipping_delay_prediction_notebook.ipynb`.

Run:
    streamlit run app.py
"""

import time
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

import styles
import utils

# ----------------------------------------------------------------------
# Page config (must be first Streamlit call)
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Shipment Delay Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

styles.inject(st)

# ----------------------------------------------------------------------
# Load artifacts / data once (cached)
# ----------------------------------------------------------------------
artifacts, missing_artifacts = utils.load_artifacts()
dataset, dataset_name = utils.load_dataset()
MODEL_READY = utils.artifacts_ready(artifacts)

FEATURE_LABELS = {
    "Weight_in_gms": "Package Weight",
    "Discount_offered": "Discount Offered",
    "Cost_of_the_Product": "Product Cost",
    "Prior_purchases": "Prior Purchases",
    "Customer_care_calls": "Customer Care Calls",
    "Product_importance": "Product Importance",
    "Mode_of_Shipment": "Mode of Shipment",
    "Warehouse_block": "Warehouse Block",
}

# ----------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------
NAV_ITEMS = [
    "🏠  Home",
    "🧭  About Project",
    "🗃️  Dataset",
    "🧠  Model Info",
    "🔮  Predict Delay",
    "📊  Analytics",
    "🌟  Feature Importance",
    "🛠️  Workflow",
    "✅  Conclusion",
]
if "nav" not in st.session_state:
    st.session_state["nav"] = NAV_ITEMS[0]

# Apply any pending navigation request (set by in-page buttons) BEFORE the
# radio widget below is instantiated -- session_state for a widget's key
# can only be reassigned prior to that widget being created in this run.
if "_nav_target" in st.session_state:
    st.session_state["nav"] = st.session_state.pop("_nav_target")

with st.sidebar:
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <div style="font-size:1.6rem;">📦</div>
            <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1.12rem;color:#EDEFF7;">
                ShipSense
            </div>
        </div>
        <div style="color:#616B84;font-size:0.78rem;margin-bottom:22px;font-family:'JetBrains Mono',monospace;">
            Shipment Delay Intelligence
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigate",
        NAV_ITEMS,
        label_visibility="collapsed",
        key="nav",
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    status_color = "#33D17A" if MODEL_READY else "#F5A524"
    status_text = "Model Online" if MODEL_READY else "Model Assets Missing"
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:8px;font-size:0.82rem;color:#9AA3B8;">
            <span style="width:8px;height:8px;border-radius:50%;background:{status_color};
                  box-shadow:0 0 8px {status_color};display:inline-block;"></span>
            {status_text}
        </div>
        """,
        unsafe_allow_html=True,
    )
    if dataset is not None:
        st.caption(f"Dataset: `{dataset_name}` · {len(dataset):,} rows")
    st.markdown(
        "<div style='margin-top:26px;color:#616B84;font-size:0.74rem;'>"
        "Built with Streamlit · scikit-learn · XGBoost</div>",
        unsafe_allow_html=True,
    )

page = page.split("  ", 1)[1] if "  " in page else page


# ----------------------------------------------------------------------
# Reusable components
# ----------------------------------------------------------------------
def metric_card(label, value, delta=None):
    delta_html = f'<div class="delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="metric">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(icon, title, text):
    st.markdown(
        f"""
        <div class="card">
            <div class="icon">{icon}</div>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def missing_assets_notice():
    st.warning(
        "Some model assets could not be found in `models/`. "
        "Copy `shipping_delay_model.pkl`, `scaler.pkl`, `warehouse_encoder.pkl`, "
        "`shipment_encoder.pkl`, and `importance_encoder.pkl` from your training "
        "output into the `models/` folder to enable predictions.\n\n"
        f"Missing: {', '.join(missing_artifacts)}"
    )


# ========================================================================
# HOME
# ========================================================================
if page == "Home":
    st.markdown(
        '<div class="eyebrow"><span class="dot"></span>ML-POWERED LOGISTICS INTELLIGENCE</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="hero-title">Know a shipment will be late<br>before it ever leaves the dock.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">ShipSense analyzes warehouse, carrier, product and customer '
        'signals to predict delivery delays before dispatch — so logistics teams can '
        'reroute, expedite, or communicate proactively instead of reacting after the fact.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(styles.route_divider(), unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("🔮  Run a Prediction", width='stretch'):
            st.session_state["_nav_target"] = "🔮  Predict Delay"
            st.rerun()
    with c2:
        if st.button("📊  Explore Analytics", width='stretch'):
            st.session_state["_nav_target"] = "📊  Analytics"
            st.rerun()

    st.markdown(styles.section_head("Why it matters", "IMPACT").replace("42px", "48px"), unsafe_allow_html=True)
    cols = st.columns(4)
    stats = [
        ("On-Time Visibility", "Pre-Dispatch", "Predict before the package ships"),
        ("Primary Metric", "F1 Score", "Balances false alarms vs missed delays"),
        ("Model Family", "Stacking Ensemble", "RandomForest + DecisionTree → LogReg"),
        ("Decision Window", "Real-Time", "Instant inference from 8 shipment signals"),
    ]
    for col, (label, value, sub) in zip(cols, stats):
        with col:
            metric_card(label, value, sub)

    st.markdown(styles.section_head("What ShipSense does", "CAPABILITIES"), unsafe_allow_html=True)
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        feature_card("🎯", "Pre-Dispatch Risk Scoring", "Every shipment gets an on-time / delay prediction with a confidence score before it leaves the warehouse.")
    with r1c2:
        feature_card("🧩", "Explainable Signals", "Feature importance shows exactly which factors — discount, weight, warehouse — are driving risk.")
    with r1c3:
        feature_card("📈", "Operational Analytics", "Interactive dashboards surface delay patterns across warehouses, carriers and product categories.")

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        feature_card("⚙️", "Production Pipeline", "Trained encoders and scaler are version-matched to the deployed model — no train/serve skew.")
    with r2c2:
        feature_card("🚚", "Carrier-Aware", "Accounts for shipment mode — Flight, Road, or Ship — alongside product and customer behaviour.")
    with r2c3:
        feature_card("🔒", "Reproducible", "Full notebook-to-deployment lineage, from EDA to hyperparameter tuning to the saved model.")

    st.markdown("<div class='foot'><span>ShipSense · Shipment Delay Intelligence</span><span>Built on a StackingClassifier · F1 ≈ 0.716</span></div>", unsafe_allow_html=True)

# ========================================================================
# ABOUT PROJECT
# ========================================================================
elif page == "About Project":
    st.markdown('<div class="eyebrow"><span class="dot"></span>PROJECT BRIEF</div>', unsafe_allow_html=True)
    st.markdown("## About the Project")
    st.write(
        "Logistics providers such as Amazon, Flipkart, DHL, FedEx and Blue Dart move "
        "thousands of shipments daily. Delays — driven by weather, traffic, carrier load, "
        "warehouse throughput or product characteristics — erode customer trust and add "
        "operational cost. ShipSense predicts delivery risk **before dispatch**, giving "
        "logistics teams a window to act instead of react."
    )

    st.markdown(styles.section_head("Business Problem", "WHY"), unsafe_allow_html=True)
    st.write("A logistics company wants to identify shipments at high risk of delay **before** they leave the warehouse, so operations teams can intervene early.")

    b1, b2 = st.columns(2)
    with b1:
        st.markdown("#### Challenges of Delivery Delays")
        for item in ["Poor customer satisfaction", "Increased operational costs", "Supply chain disruptions", "Negative reviews & loss of trust"]:
            st.markdown(f"- {item}")
    with b2:
        st.markdown("#### Business Benefits")
        for item in ["Improved delivery planning", "Fewer late deliveries", "Optimized shipping operations", "Higher customer satisfaction", "Lower operational costs", "Data-driven decision making"]:
            st.markdown(f"- {item}")

    st.markdown(styles.section_head("Problem Statement", "GOAL"), unsafe_allow_html=True)
    st.info(
        "**Predict whether a shipment will be delivered on time or delayed, before dispatch**, "
        "using warehouse, shipment-mode, product and customer-behaviour features."
    )

    st.markdown(styles.section_head("Why F1 Score", "METRIC CHOICE"), unsafe_allow_html=True)
    st.write(
        "The project optimizes for **F1 Score** rather than raw accuracy. A false positive "
        "(predicting a delay that doesn't happen) triggers unnecessary operational action; a "
        "false negative (missing a real delay) causes unhappy customers and downstream "
        "disruption. F1 balances both error types rather than favoring one."
    )

# ========================================================================
# DATASET
# ========================================================================
elif page == "Dataset":
    st.markdown('<div class="eyebrow"><span class="dot"></span>DATA</div>', unsafe_allow_html=True)
    st.markdown("## Dataset Information")

    if dataset is not None:
        c1, c2, c3, c4 = st.columns(4)
        with c1: metric_card("Rows", f"{len(dataset):,}")
        with c2: metric_card("Columns", f"{dataset.shape[1]}")
        with c3: metric_card("Missing Values", f"{int(dataset.isnull().sum().sum())}")
        with c4: metric_card("Duplicate Rows", f"{int(dataset.duplicated().sum())}")

        st.markdown(styles.section_head("Preview", dataset_name), unsafe_allow_html=True)
        st.dataframe(dataset.sample(min(12, len(dataset)), random_state=42), width='stretch')

        st.markdown(styles.section_head("Column Types", "SCHEMA"), unsafe_allow_html=True)
        dtype_df = pd.DataFrame({
            "Column": dataset.columns,
            "Dtype": dataset.dtypes.astype(str).values,
            "Unique Values": [dataset[c].nunique() for c in dataset.columns],
        })
        st.dataframe(dtype_df, width='stretch', hide_index=True)
    else:
        st.warning(
            "No dataset file found in `data/`. Add `cleaned.csv` (or `raw_data.csv`) "
            "to enable this section."
        )

    st.markdown(styles.section_head("Feature Reference", "USED IN MODEL"), unsafe_allow_html=True)
    ref = pd.DataFrame([
        ["Warehouse_block", "Categorical", "Kept", "5 warehouse zones (A–D, F)"],
        ["Mode_of_Shipment", "Categorical", "Kept", "Flight / Road / Ship"],
        ["Customer_care_calls", "Numeric", "Kept", "Support calls made for this order"],
        ["Customer_rating", "Numeric", "Dropped", "Given post-delivery → data leakage"],
        ["Cost_of_the_Product", "Numeric", "Kept", "May affect shipping priority"],
        ["Prior_purchases", "Numeric", "Kept", "Customer purchase history"],
        ["Product_importance", "Categorical", "Kept", "low / medium / high"],
        ["Gender", "Categorical", "Dropped", "No meaningful relationship to delay"],
        ["Discount_offered", "Numeric", "Kept", "Can influence shipping behaviour"],
        ["Weight_in_gms", "Numeric", "Kept", "Directly affects shipping time"],
        ["Reached.on.Time_Y.N", "Target", "Target", "1 = delayed, 0 = on time"],
    ], columns=["Feature", "Type", "Decision", "Rationale"])
    st.dataframe(ref, width='stretch', hide_index=True)

# ========================================================================
# MODEL INFO
# ========================================================================
elif page == "Model Info":
    st.markdown('<div class="eyebrow"><span class="dot"></span>MODELING</div>', unsafe_allow_html=True)
    st.markdown("## Model Information")

    st.write(
        "Ten classification models were trained and compared on Accuracy, Precision, "
        "Recall and F1 Score. The top three by F1 — **Stacking Classifier**, **AdaBoost**, "
        "and **XGBoost** — were tuned with `RandomizedSearchCV` and `GridSearchCV`."
    )

    leaderboard = pd.DataFrame([
        ["Stacking Classifier", 0.7157, "Default params — selected for deployment"],
        ["AdaBoost", 0.7051, "Tuned, competitive but lower F1"],
        ["XGBoost", 0.7030, "Tuned, competitive but lower F1"],
        ["Random Forest", "—", "Used for feature importance analysis"],
        ["Gradient Boosting", "—", "Baseline ensemble comparison"],
        ["Logistic Regression", "—", "Linear baseline (scaled features)"],
        ["KNN", "—", "Distance-based baseline (scaled features)"],
        ["SVM", "—", "Margin-based baseline (scaled features)"],
        ["Decision Tree", "—", "Single-tree baseline"],
        ["Gaussian Naive Bayes", "—", "Probabilistic baseline"],
    ], columns=["Model", "F1 Score", "Notes"])
    st.markdown(styles.section_head("Model Leaderboard", "F1-RANKED"), unsafe_allow_html=True)
    st.dataframe(leaderboard, width='stretch', hide_index=True)

    st.markdown(styles.section_head("Deployed Model", "PRODUCTION"), unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1: metric_card("Algorithm", "Stacking Ensemble")
    with m2: metric_card("Base Learners", "RandomForest + DecisionTree")
    with m3: metric_card("Final Estimator", "Logistic Regression")

    st.markdown(
        """
        <div class="card" style="margin-top:18px;">
            <h3>Why a Stacking Classifier?</h3>
            <p>The stacking ensemble combines a Random Forest and a Decision Tree as base
            learners, with a Logistic Regression meta-model learning how to best combine
            their outputs. Hyperparameter tuning on the top 3 candidates did not beat the
            default stacking configuration on the held-out test set, so it was kept as the
            final model with an F1 Score of <b>0.7157</b>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(styles.section_head("Serving Pipeline", "ARTIFACTS"), unsafe_allow_html=True)
    pipe_cols = st.columns(5)
    pipe_steps = [
        ("1", "Warehouse Encoder", "warehouse_encoder.pkl"),
        ("2", "Shipment Encoder", "shipment_encoder.pkl"),
        ("3", "Importance Encoder", "importance_encoder.pkl"),
        ("4", "Feature Scaler", "scaler.pkl"),
        ("5", "Stacking Model", "shipping_delay_model.pkl"),
    ]
    for col, (n, title, fname) in zip(pipe_cols, pipe_steps):
        ok = fname in [p.name for p in utils.MODEL_FILES.values() if p.exists()]
        badge = '<span class="badge teal">loaded</span>' if ok else '<span class="badge">missing</span>'
        with col:
            st.markdown(
                f"""<div class="card" style="text-align:center;padding:18px 12px;">
                <div class="mono" style="color:#616B84;font-size:0.72rem;">STEP {n}</div>
                <div style="font-weight:600;margin:6px 0 8px 0;">{title}</div>
                {badge}
                </div>""",
                unsafe_allow_html=True,
            )

    if not MODEL_READY:
        missing_assets_notice()

# ========================================================================
# PREDICT DELAY
# ========================================================================
elif page == "Predict Delay":
    st.markdown('<div class="eyebrow"><span class="dot"></span>LIVE INFERENCE</div>', unsafe_allow_html=True)
    st.markdown("## Predict Shipment Delay")
    st.write("Enter shipment details below. Prediction runs through the exact same encoders and model saved from training.")

    if not MODEL_READY:
        missing_assets_notice()

    with st.form("predict_form"):
        st.markdown("#### Shipment Details")
        f1, f2, f3 = st.columns(3)
        with f1:
            warehouse = st.selectbox("Warehouse Block", utils.CATEGORY_OPTIONS["Warehouse_block"])
            shipment_mode = st.selectbox("Mode of Shipment", utils.CATEGORY_OPTIONS["Mode_of_Shipment"])
        with f2:
            importance = st.selectbox("Product Importance", utils.CATEGORY_OPTIONS["Product_importance"])
            care_calls = st.slider("Customer Care Calls", 0, 10, 4)
        with f3:
            prior_purchases = st.slider("Prior Purchases", 0, 15, 3)
            discount = st.slider("Discount Offered (%)", 0, 70, 10)

        st.markdown("#### Product Details")
        g1, g2 = st.columns(2)
        with g1:
            cost = st.number_input("Cost of the Product ($)", min_value=1, max_value=5000, value=210)
        with g2:
            weight = st.number_input("Weight (grams)", min_value=100, max_value=10000, value=3500)

        submitted = st.form_submit_button("🔮  Predict Delay Risk", width='stretch')

    if submitted:
        if not MODEL_READY:
            st.error("Cannot run prediction — required model assets are missing. See notice above.")
        else:
            raw_inputs = {
                "Warehouse_block": warehouse,
                "Mode_of_Shipment": shipment_mode,
                "Customer_care_calls": care_calls,
                "Cost_of_the_Product": cost,
                "Prior_purchases": prior_purchases,
                "Product_importance": importance,
                "Discount_offered": discount,
                "Weight_in_gms": weight,
            }

            with st.spinner("Scoring shipment..."):
                time.sleep(0.5)
                result = utils.predict_delay(raw_inputs, artifacts)

            is_delayed = result["is_delayed"]
            proba = result["probability"]

            st.markdown(styles.route_divider(), unsafe_allow_html=True)

            if is_delayed:
                risk_pct = utils.fmt_pct(proba) if proba is not None else "High"
                st.markdown(
                    f"""
                    <div class="result delay">
                        <span class="badge" style="border-color:#F5455C;color:#F5455C;">⚠ AT RISK</span>
                        <div class="headline" style="margin-top:12px;">Likely to be Delayed</div>
                        <div class="sub">Model confidence of delay: <b>{risk_pct}</b></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                confident_pct = utils.fmt_pct(1 - proba) if proba is not None else "High"
                st.markdown(
                    f"""
                    <div class="result ontime">
                        <span class="badge" style="border-color:#33D17A;color:#33D17A;">✓ ON TRACK</span>
                        <div class="headline" style="margin-top:12px;">Likely to Arrive On Time</div>
                        <div class="sub">Model confidence of on-time delivery: <b>{confident_pct}</b></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            cols = st.columns(3)
            with cols[0]:
                metric_card("Prediction", "Delayed" if is_delayed else "On Time")
            with cols[1]:
                metric_card("Delay Probability", utils.fmt_pct(proba) if proba is not None else "N/A")
            with cols[2]:
                metric_card("Risk Tier", "High" if (proba or 0) > 0.66 else "Moderate" if (proba or 0) > 0.33 else "Low")

            if proba is not None:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=proba * 100,
                    number={"suffix": "%", "font": {"color": "#EDEFF7", "family": "Space Grotesk"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "#616B84"},
                        "bar": {"color": "#F5455C" if is_delayed else "#33D17A"},
                        "bgcolor": "#131a2b",
                        "borderwidth": 0,
                        "steps": [
                            {"range": [0, 33], "color": "rgba(51,209,122,0.18)"},
                            {"range": [33, 66], "color": "rgba(245,165,36,0.18)"},
                            {"range": [66, 100], "color": "rgba(245,69,92,0.18)"},
                        ],
                    },
                    title={"text": "Delay Risk", "font": {"color": "#9AA3B8", "size": 14}},
                ))
                fig.update_layout(
                    height=280, margin=dict(l=20, r=20, t=40, b=10),
                    paper_bgcolor="rgba(0,0,0,0)", font_color="#EDEFF7",
                )
                st.plotly_chart(fig, width='stretch')

            with st.expander("How to read this result"):
                st.write(
                    "The model was trained on historical shipments where warehouse zone, "
                    "shipment mode, customer behaviour and product characteristics were "
                    "associated with late or on-time delivery. A **higher delay probability** "
                    "means the current combination of inputs resembles shipments that were "
                    "historically delayed more often — it is a risk signal, not a guarantee."
                )

# ========================================================================
# ANALYTICS
# ========================================================================
elif page == "Analytics":
    st.markdown('<div class="eyebrow"><span class="dot"></span>EXPLORATORY ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown("## Delay Analytics")

    if dataset is None:
        st.warning("No dataset found in `data/`. Add `cleaned.csv` to enable interactive analytics.")
    else:
        df = dataset.copy()
        target_col = "Reached.on.Time_Y.N"

        if target_col in df.columns:
            delay_rate = df[target_col].mean()
            c1, c2, c3 = st.columns(3)
            with c1: metric_card("Total Shipments", f"{len(df):,}")
            with c2: metric_card("Delay Rate", utils.fmt_pct(delay_rate))
            with c3: metric_card("On-Time Rate", utils.fmt_pct(1 - delay_rate))

            tabs = st.tabs(["Warehouse", "Shipment Mode", "Product Importance", "Weight vs Delay", "Discount vs Delay"])

            with tabs[0]:
                if "Warehouse_block" in df.columns:
                    grp = df.groupby("Warehouse_block")[target_col].mean().reset_index()
                    fig = px.bar(grp, x="Warehouse_block", y=target_col, color=target_col,
                                 color_continuous_scale=["#33D17A", "#F5A524", "#F5455C"],
                                 labels={target_col: "Delay Rate"})
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                       font_color="#EDEFF7", height=380)
                    st.plotly_chart(fig, width='stretch')

            with tabs[1]:
                if "Mode_of_Shipment" in df.columns:
                    grp = df.groupby("Mode_of_Shipment")[target_col].mean().reset_index()
                    fig = px.bar(grp, x="Mode_of_Shipment", y=target_col, color=target_col,
                                 color_continuous_scale=["#33D17A", "#F5A524", "#F5455C"],
                                 labels={target_col: "Delay Rate"})
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                       font_color="#EDEFF7", height=380)
                    st.plotly_chart(fig, width='stretch')

            with tabs[2]:
                if "Product_importance" in df.columns:
                    grp = df.groupby("Product_importance")[target_col].mean().reset_index()
                    fig = px.bar(grp, x="Product_importance", y=target_col, color=target_col,
                                 color_continuous_scale=["#33D17A", "#F5A524", "#F5455C"],
                                 labels={target_col: "Delay Rate"})
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                       font_color="#EDEFF7", height=380)
                    st.plotly_chart(fig, width='stretch')

            with tabs[3]:
                if "Weight_in_gms" in df.columns:
                    fig = px.histogram(df, x="Weight_in_gms", color=df[target_col].map({0: "On Time", 1: "Delayed"}),
                                        barmode="overlay", nbins=40,
                                        color_discrete_map={"On Time": "#33D17A", "Delayed": "#F5455C"})
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                       font_color="#EDEFF7", height=380, legend_title_text="")
                    st.plotly_chart(fig, width='stretch')

            with tabs[4]:
                if "Discount_offered" in df.columns:
                    fig = px.histogram(df, x="Discount_offered", color=df[target_col].map({0: "On Time", 1: "Delayed"}),
                                        barmode="overlay", nbins=40,
                                        color_discrete_map={"On Time": "#33D17A", "Delayed": "#F5455C"})
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                       font_color="#EDEFF7", height=380, legend_title_text="")
                    st.plotly_chart(fig, width='stretch')
        else:
            st.info("Target column `Reached.on.Time_Y.N` not found in this dataset file — showing raw preview instead.")
            st.dataframe(df.head(20), width='stretch')

    st.markdown(styles.section_head("Saved Notebook Graphs", "PRE-COMPUTED"), unsafe_allow_html=True)
    graph_files = [
        ("Customer_care_calls_Boxplot.png", "Customer Care Calls"),
        ("Customer_rating_Boxplot.png", "Customer Rating"),
        ("Cost_of_the_Product_Boxplot.png", "Cost of the Product"),
        ("Prior_purchases_Boxplot.png", "Prior Purchases"),
        ("Discount_offered_Boxplot.png", "Discount Offered"),
        ("Weight_in_gms_Boxplot.png", "Weight (grams)"),
    ]
    cols = st.columns(3)
    any_found = False
    for i, (fname, label) in enumerate(graph_files):
        p = utils.graph_path(fname)
        with cols[i % 3]:
            if p:
                any_found = True
                st.image(str(p), caption=f"{label} — Outlier Check", width='stretch')
            else:
                st.markdown(
                    f"""<div class="card" style="text-align:center;color:#616B84;">
                    <p>{label}<br><span class="mono" style="font-size:0.72rem;">graphs/{fname} not found</span></p>
                    </div>""",
                    unsafe_allow_html=True,
                )
    if not any_found:
        st.caption("Add your saved PNGs to `graphs/` to display them here.")

# ========================================================================
# FEATURE IMPORTANCE
# ========================================================================
elif page == "Feature Importance":
    st.markdown('<div class="eyebrow"><span class="dot"></span>MODEL EXPLAINABILITY</div>', unsafe_allow_html=True)
    st.markdown("## Feature Importance")
    st.write("Which shipment signals most influence the model's predictions, computed from a Random Forest trained on the same feature set.")

    saved_fi = utils.graph_path("Feature_Importance.png")
    if saved_fi:
        st.image(str(saved_fi), caption="Feature Importance (from notebook)", width='stretch')
    elif dataset is not None and "Reached.on.Time_Y.N" in dataset.columns and MODEL_READY:
        st.caption("Precomputed graph not found — generating live from the current dataset.")
        try:
            from sklearn.ensemble import RandomForestClassifier

            df = dataset.copy()
            wh = artifacts["warehouse_encoder"]
            sm = artifacts["shipment_encoder"]
            pi = artifacts["importance_encoder"]
            df["Warehouse_block"] = wh.transform(df["Warehouse_block"])
            df["Mode_of_Shipment"] = sm.transform(df["Mode_of_Shipment"])
            df["Product_importance"] = pi.transform(df["Product_importance"])
            X = df[utils.FEATURE_ORDER]
            y = df["Reached.on.Time_Y.N"]

            rf = RandomForestClassifier(random_state=42)
            rf.fit(X, y)
            fi = pd.DataFrame({"Feature": X.columns, "Importance": rf.feature_importances_}).sort_values("Importance", ascending=True)
            fi["Feature"] = fi["Feature"].map(lambda f: FEATURE_LABELS.get(f, f))

            fig = px.bar(fi, x="Importance", y="Feature", orientation="h",
                         color="Importance", color_continuous_scale=["#2DD4BF", "#6C63FF"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               font_color="#EDEFF7", height=420, showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig, width='stretch')
        except Exception as e:  # noqa: BLE001
            st.error(f"Could not compute feature importance live: {e}")
    else:
        st.info("Add `Feature_Importance.png` to `graphs/`, or ensure both the dataset and model assets are available to compute it live.")

    st.markdown(
        """
        <div class="card" style="margin-top:18px;">
            <h3>Reading the chart</h3>
            <p>Longer bars indicate features the Random Forest relied on most heavily when
            splitting shipments into delayed vs. on-time groups. In this project,
            <b>Discount_offered</b> and <b>Weight_in_gms</b> are typically the strongest
            signals, followed by <b>Cost_of_the_Product</b> and <b>Prior_purchases</b> —
            warehouse and shipment mode tend to contribute less on their own.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ========================================================================
# WORKFLOW
# ========================================================================
elif page == "Workflow":
    st.markdown('<div class="eyebrow"><span class="dot"></span>END-TO-END PIPELINE</div>', unsafe_allow_html=True)
    st.markdown("## Project Workflow")
    st.write("From raw data to a deployed application — the full pipeline followed in the notebook.")

    steps = [
        ("01", "Business Understanding", "Framed the problem: predict delay risk before dispatch to reduce cost and improve customer experience."),
        ("02", "Data Collection & Understanding", "Loaded the raw shipment dataset and profiled column types, cardinality, and target balance."),
        ("03", "Data Cleaning", "Checked for missing values and duplicates — the dataset required no imputation or row removal."),
        ("04", "Outlier Review", "Boxplots inspected across numeric features; outliers in fields like Discount_offered were kept as legitimate variation."),
        ("05", "Feature Engineering & Selection", "Dropped ID, Gender and Customer_rating (post-delivery leakage); kept 8 predictive features."),
        ("06", "Encoding", "Label-encoded Warehouse_block, Mode_of_Shipment and Product_importance; encoders saved for serving."),
        ("07", "Train/Test Split & Scaling", "80/20 split with a fixed random state; StandardScaler fit on the training set for scale-sensitive models."),
        ("08", "Model Training", "Trained 10 classifiers spanning linear, distance-based, probabilistic, tree and ensemble families."),
        ("09", "Model Comparison", "Ranked all models by F1 Score; Stacking Classifier, AdaBoost and XGBoost emerged as top 3."),
        ("10", "Hyperparameter Tuning", "RandomizedSearchCV and GridSearchCV applied to the top 3 candidates."),
        ("11", "Final Model Selection", "Default Stacking Classifier retained the best F1 Score (0.7157) even after tuning attempts."),
        ("12", "Explainability", "Random Forest feature importances computed to interpret key delay drivers."),
        ("13", "Persistence", "Model, scaler and encoders serialized with joblib for reproducible serving."),
        ("14", "Deployment", "Wrapped in this Streamlit application for interactive, real-time predictions."),
    ]
    for n, title, desc in steps:
        st.markdown(
            f"""<div class="step">
                <div class="n">{n}</div>
                <div>
                    <div class="t">{title}</div>
                    <div class="d">{desc}</div>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

# ========================================================================
# CONCLUSION
# ========================================================================
elif page == "Conclusion":
    st.markdown('<div class="eyebrow"><span class="dot"></span>SUMMARY</div>', unsafe_allow_html=True)
    st.markdown("## Conclusion")
    st.write(
        "ShipSense demonstrates a complete, production-shaped machine learning workflow — "
        "from EDA and leakage-aware feature selection through model comparison, tuning, and "
        "deployment. The final Stacking Classifier balances precision and recall well enough "
        "to serve as an early-warning system for shipment delays, and the interactive "
        "prediction and analytics views make its reasoning inspectable rather than a black box."
    )

    st.markdown(styles.section_head("Key Takeaways", "RESULTS"), unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        feature_card("🏆", "Best Model", "Stacking Classifier (RF + DT → LogReg) with F1 Score 0.7157 on the held-out test set.")
    with cols[1]:
        feature_card("🔍", "Top Drivers", "Discount offered and package weight were consistently the strongest delay signals.")
    with cols[2]:
        feature_card("🧭", "No Leakage", "Customer_rating was excluded since it's only known after delivery — a common pitfall avoided here.")

    st.markdown(styles.section_head("Possible Extensions", "NEXT STEPS"), unsafe_allow_html=True)
    for item in [
        "Incorporate real-time weather and traffic data for dynamic risk scoring",
        "Add carrier-level and route-level historical performance features",
        "Calibrate probabilities (e.g. Platt scaling) for more reliable confidence scores",
        "Set up drift monitoring as new shipment data arrives in production",
    ]:
        st.markdown(f"- {item}")

    st.markdown(styles.route_divider(), unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;color:#9AA3B8;'>Thank you for exploring ShipSense — "
        "a shipment delay intelligence system built end-to-end from notebook to deployment.</p>",
        unsafe_allow_html=True,
    )