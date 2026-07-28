import os
import sys

import numpy as np
import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import components as C
import data_utils as D
import style

st.set_page_config(
    page_title="Fraud Sentinel — Credit Card Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

style.inject(st)

# ----------------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        "<div style='font-family:Cormorant Garamond,serif; font-size:1.6rem; "
        "font-weight:700; color:#E4C55E;'>🛡️ Fraud Sentinel</div>"
        "<div style='font-family:JetBrains Mono,monospace; font-size:0.68rem; "
        "letter-spacing:0.1em; color:#8A8F9C; margin-bottom:1.2rem;'>"
        "CREDIT CARD FRAUD DETECTION</div>",
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Navigate",
        ["Overview", "Predict", "Analytics", "Model Performance", "About"],
        label_visibility="collapsed",
    )
    st.markdown("<div class='gold-rule'></div>", unsafe_allow_html=True)
    try:
        metrics = D.load_metrics()
        st.markdown(
            f"<div style='font-family:JetBrains Mono,monospace; font-size:0.72rem; color:#8A8F9C;'>"
            f"MODEL STATUS<br><span style='color:#2FBF89;'>● live</span> &nbsp;|&nbsp; "
            f"ROC-AUC {metrics['roc_auc']:.3f}</div>",
            unsafe_allow_html=True,
        )
    except Exception:
        pass
    st.markdown(
        "<div style='font-family:JetBrains Mono,monospace; font-size:0.68rem; "
        "color:#5b5f6a; margin-top:2rem;'>Portfolio project · not for production use</div>",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Page: Overview
# ----------------------------------------------------------------------------
def page_overview():
    try:
        sample_df = D.load_sample_transactions()
        ticker_rows = C.build_ticker_rows(sample_df)
    except Exception:
        ticker_rows = None

    st.markdown(
        C.hero(
            "Fraud Sentinel",
            "A PyTorch neural network that screens credit-card transactions for fraud in "
            "real time — trained on 339,607 real transactions spanning 14 merchant "
            "categories, 13 states, and a 189-to-1 legitimate-to-fraud imbalance.",
            ticker_rows,
        ),
        unsafe_allow_html=True,
    )

    metrics = D.load_metrics()
    cards = [
        C.metric_card("Transactions Analyzed", "339,607", "training + validation + test"),
        C.metric_card("Fraud Rate", "0.52%", "1,782 confirmed fraud cases", accent="oxblood"),
        C.metric_card("Model Accuracy", f"{metrics['accuracy']*100:.2f}%", "held-out test set", accent="emerald"),
        C.metric_card("ROC-AUC", f"{metrics['roc_auc']:.3f}", "risk-ranking quality", accent="emerald"),
    ]
    st.markdown(C.card_row(cards), unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown(
            C.panel_open("How it works")
            + "<p style='color:#C8C3B8; line-height:1.6;'>Every transaction is described by 11 features — "
              "merchant, category, amount, cardholder location and job, and merchant location. "
              "A compact feed-forward network (<span class='pill'>11 → 16 → 8 → 1</span>) "
              "scores each transaction's fraud probability. You set the decision threshold; "
              "the model does the ranking.</p>"
              "<p style='color:#8A8F9C; font-size:0.85rem;'>Because fraud is only 0.52% of "
              "transactions, the model is tuned to rank risk well (ROC-AUC "
              f"{metrics['roc_auc']:.3f}) even though its recall at the default threshold is "
              "modest — see <b>Model Performance</b> for the honest breakdown.</p>"
            + C.panel_close(),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            C.panel_open("Try it now")
            + "<p style='color:#C8C3B8;'>Head to the <b>Predict</b> tab to score a single "
              "transaction, load a real sample, or upload a batch of transactions for scoring.</p>"
            + C.panel_close(),
            unsafe_allow_html=True,
        )
        if st.button("Go to Predict →", width='stretch', type="primary"):
            st.session_state["_nav_hint"] = "Predict"
            st.rerun()

    st.markdown("<div class='gold-rule'></div>", unsafe_allow_html=True)
    st.markdown("#### Dataset snapshot")
    try:
        preview = D.load_full_data(n_rows=2000)
        st.dataframe(preview.head(8), width='stretch', hide_index=True)
    except Exception:
        st.info("Dataset preview unavailable in this environment.")


# ----------------------------------------------------------------------------
# Page: Predict
# ----------------------------------------------------------------------------
def page_predict():
    st.markdown(
        "<div class='eyebrow'>Score a transaction</div>"
        "<h1 style='margin-top:0;'>Predict</h1>",
        unsafe_allow_html=True,
    )

    predictor = D.load_predictor()
    city_lookup = D.load_city_lookup()
    merchant_lookup = D.load_merchant_lookup()
    job_list = D.load_job_list()
    categories = D.load_categories()
    cities = sorted(city_lookup.keys())
    merchants = sorted(merchant_lookup.keys())

    tab_single, tab_batch = st.tabs(["🔎 Single transaction", "📁 Batch upload"])

    with tab_single:
        left, right = st.columns([1, 1.15])

        if "form_defaults" not in st.session_state:
            st.session_state.form_defaults = None

        with left:
            st.markdown(C.panel_open("Transaction details"), unsafe_allow_html=True)
            if st.button("🎲 Load a random real transaction", width='stretch'):
                sample = D.load_sample_transactions().sample(1).iloc[0]
                st.session_state.form_defaults = sample.to_dict()
                st.rerun()

            defaults = st.session_state.form_defaults or {}

            category = st.selectbox(
                "Merchant category", categories,
                index=categories.index(defaults["category"]) if defaults.get("category") in categories else 0,
            )
            amt = st.number_input(
                "Transaction amount ($)", min_value=0.01, max_value=50000.0,
                value=float(defaults.get("amt", 45.0)), step=1.0,
            )
            merchant = st.selectbox(
                "Merchant", merchants,
                index=merchants.index(defaults["merchant"]) if defaults.get("merchant") in merchants else 0,
            )
            city = st.selectbox(
                "Cardholder city", cities,
                index=cities.index(defaults["city"]) if defaults.get("city") in cities else 0,
            )
            city_info = city_lookup[city]
            job_default = defaults.get("job", job_list[0])
            job = st.selectbox(
                "Cardholder occupation", job_list,
                index=job_list.index(job_default) if job_default in job_list else 0,
            )

            with st.expander("Advanced — geolocation (auto-filled from city / merchant)"):
                state = st.text_input("State", value=city_info["state"], disabled=True)
                lat = st.number_input("Cardholder latitude", value=float(city_info["lat"]))
                long = st.number_input("Cardholder longitude", value=float(city_info["long"]))
                city_pop = st.number_input(
                    "City population", min_value=1, value=int(city_info["city_pop"])
                )
                m_info = merchant_lookup[merchant]
                merch_lat = st.number_input("Merchant latitude", value=float(m_info["merch_lat"]))
                merch_long = st.number_input("Merchant longitude", value=float(m_info["merch_long"]))

            threshold = st.slider(
                "Decision threshold", min_value=0.05, max_value=0.95, value=0.50, step=0.05,
                help="Lower this to catch more fraud at the cost of more false alarms.",
            )
            predict_clicked = st.button("🛡️ Score this transaction", type="primary", width='stretch')
            st.markdown(C.panel_close(), unsafe_allow_html=True)

        with right:
            if predict_clicked:
                row = pd.DataFrame([{
                    "merchant": merchant, "category": category, "amt": amt,
                    "city": city, "state": state, "lat": lat, "long": long,
                    "city_pop": city_pop, "job": job,
                    "merch_lat": merch_lat, "merch_long": merch_long,
                }])
                probs, preds = predictor.predict(row, threshold=threshold)
                prob = float(probs[0])

                st.markdown(C.panel_open("Verdict"), unsafe_allow_html=True)
                st.markdown(C.verdict_seal(prob, threshold), unsafe_allow_html=True)
                st.markdown(C.panel_close(), unsafe_allow_html=True)

                st.progress(min(max(prob, 0.0), 1.0), text=f"Fraud probability — {prob*100:.1f}%")

                if st.session_state.get("form_defaults"):
                    true_label = st.session_state.form_defaults.get("is_fraud")
                    if true_label is not None:
                        actual = "Fraud" if true_label == 1 else "Legitimate"
                        st.caption(f"Ground truth for this loaded sample: **{actual}**")

                with st.expander("Raw feature values sent to the model"):
                    display_row = row.T.rename(columns={0: "value"})
                    display_row["value"] = display_row["value"].astype(str)
                    st.dataframe(display_row, width='stretch')
            else:
                st.markdown(
                    C.panel_open("Verdict")
                    + "<p style='color:#8A8F9C;'>Fill in the transaction details and click "
                      "<b>Score this transaction</b> to see the fraud probability here.</p>"
                    + C.panel_close(),
                    unsafe_allow_html=True,
                )

    with tab_batch:
        st.markdown(
            C.panel_open("Batch scoring")
            + "<p style='color:#C8C3B8;'>Upload a CSV with columns: "
              "<span class='pill'>merchant, category, amt, city, state, lat, long, "
              "city_pop, job, merch_lat, merch_long</span></p>"
            + C.panel_close(),
            unsafe_allow_html=True,
        )
        batch_threshold = st.slider("Batch decision threshold", 0.05, 0.95, 0.50, 0.05, key="batch_thresh")
        uploaded = st.file_uploader("Upload transactions CSV", type=["csv"])
        use_sample = st.button("Or try it with the bundled sample transactions")

        df_in = None
        if uploaded is not None:
            df_in = pd.read_csv(uploaded)
        elif use_sample:
            df_in = D.load_sample_transactions().drop(columns=["is_fraud"], errors="ignore")

        if df_in is not None:
            try:
                probs, preds = predictor.predict(df_in, threshold=batch_threshold)
                out = df_in.copy()
                out["fraud_probability"] = probs
                out["prediction"] = np.where(preds == 1, "Fraud", "Legitimate")

                n_flagged = int(preds.sum())
                cards = [
                    C.metric_card("Rows Scored", f"{len(out):,}"),
                    C.metric_card("Flagged as Fraud", f"{n_flagged:,}", accent="oxblood"),
                    C.metric_card("Flag Rate", f"{n_flagged/len(out)*100:.2f}%", accent="oxblood"),
                ]
                st.markdown(C.card_row(cards), unsafe_allow_html=True)
                st.dataframe(out, width='stretch', hide_index=True)
                st.download_button(
                    "⬇ Download scored CSV", out.to_csv(index=False).encode(),
                    file_name="scored_transactions.csv", mime="text/csv",
                )
            except Exception as e:
                st.error(f"Couldn't score this file — check the column names match. ({e})")


# ----------------------------------------------------------------------------
# Page: Analytics
# ----------------------------------------------------------------------------
def page_analytics():
    st.markdown(
        "<div class='eyebrow'>Exploratory data analysis</div>"
        "<h1 style='margin-top:0;'>Analytics</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        C.panel_open("Target distribution")
        + "<p style='color:#8A8F9C;'>Fraud makes up only 0.52% of all transactions — "
          "the central challenge this model has to work around.</p>"
        + C.panel_close(),
        unsafe_allow_html=True,
    )
    st.image(D.image_path("01_target_distribution.png"), width='stretch')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Amount distribution")
        st.image(D.image_path("02_amount_distribution.png"), width='stretch')
        st.caption("Fraudulent transactions average ~$518 vs ~$68 for legitimate ones.")
    with col2:
        st.markdown("#### Correlation heatmap")
        st.image(D.image_path("05_correlation_heatmap.png"), width='stretch')
        st.caption("No single numeric feature is strongly linearly correlated with fraud in isolation.")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### Fraud rate by category")
        st.image(D.image_path("03_category_fraud_rate.png"), width='stretch')
    with col4:
        st.markdown("#### Fraud rate by state")
        st.image(D.image_path("04_state_fraud_rate.png"), width='stretch')

    st.markdown("<div class='gold-rule'></div>", unsafe_allow_html=True)
    st.markdown(
        C.panel_open("Key observations")
        + """<ul style='color:#C8C3B8; line-height:1.8;'>
        <li><b style='color:#D1495B;'>Extreme class imbalance</b> — 1 fraud for every ~189 legitimate transactions.</li>
        <li><b style='color:#2FBF89;'>Amount is the strongest signal</b> — fraud transactions run ~7.6x higher on average.</li>
        <li><b style='color:#C9A227;'>Category matters</b> — online/card-not-present categories (shopping_net, misc_net) skew riskier.</li>
        <li><b>Geography has mild signal</b> — weaker than amount or category, but not negligible.</li>
        </ul>"""
        + C.panel_close(),
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Page: Model Performance
# ----------------------------------------------------------------------------
def page_performance():
    st.markdown(
        "<div class='eyebrow'>Held-out test set — 50,942 transactions</div>"
        "<h1 style='margin-top:0;'>Model Performance</h1>",
        unsafe_allow_html=True,
    )

    metrics = D.load_metrics()
    cards = [
        C.metric_card("Accuracy", f"{metrics['accuracy']*100:.2f}%", "misleading alone — see note below"),
        C.metric_card("Fraud Precision", f"{metrics['precision']*100:.1f}%", "of flags that are real fraud", accent="emerald"),
        C.metric_card("Fraud Recall", f"{metrics['recall']*100:.1f}%", "of fraud actually caught", accent="oxblood"),
        C.metric_card("ROC-AUC", f"{metrics['roc_auc']:.3f}", "risk-ranking quality", accent="emerald"),
    ]
    st.markdown(C.card_row(cards), unsafe_allow_html=True)

    st.markdown(
        C.panel_open("⚠ Reading these numbers honestly")
        + "<p style='color:#C8C3B8; line-height:1.6;'>With fraud at just 0.52% of transactions, a model "
          "that predicts \"legitimate\" for everything would already score ~99.5% accuracy while catching "
          "zero fraud. <b>Recall (32.8%)</b> is the real bottleneck here — at the default 0.5 threshold the "
          "model catches about 1 in 3 fraud cases, because it was trained with a plain loss function "
          "(no class weighting) against a ~189:1 imbalance. The ROC-AUC of 0.91 shows the underlying risk "
          "ranking is genuinely good — lowering the decision threshold (try it on the Predict page) trades "
          "some precision for meaningfully higher recall.</p>"
        + C.panel_close(),
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Confusion matrix")
        st.image(D.image_path("06_confusion_matrix.png"), width='stretch')
    with col2:
        st.markdown("#### ROC curve")
        st.image(D.image_path("07_roc_curve.png"), width='stretch')

    st.markdown("<div class='gold-rule'></div>", unsafe_allow_html=True)
    st.markdown("#### Classification report")
    report_df = pd.DataFrame({
        "class": ["Legitimate", "Fraud"],
        "precision": [0.9965, metrics["precision"]],
        "recall": [0.9994, metrics["recall"]],
        "f1-score": [0.9979, metrics["f1_score"]],
        "support": [50674, metrics["fraud_in_test"]],
    })
    st.dataframe(report_df, width='stretch', hide_index=True)


# ----------------------------------------------------------------------------
# Page: About
# ----------------------------------------------------------------------------
def page_about():
    st.markdown(
        "<div class='eyebrow'>Project details</div>"
        "<h1 style='margin-top:0;'>About</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        C.panel_open("Business problem")
        + "<p style='color:#C8C3B8; line-height:1.6;'>Card issuers need to flag fraudulent transactions "
          "quickly enough to block them, without drowning legitimate cardholders in false declines. This "
          "project builds a screening model over 339,607 real transactions to explore that trade-off.</p>"
        + C.panel_close(),
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            C.panel_open("Model architecture")
            + """<table style='width:100%; color:#C8C3B8; font-family:JetBrains Mono,monospace; font-size:0.85rem;'>
            <tr><td>Input features</td><td>11</td></tr>
            <tr><td>Hidden layer 1</td><td>16 units, ReLU</td></tr>
            <tr><td>Hidden layer 2</td><td>8 units, ReLU</td></tr>
            <tr><td>Output</td><td>1 logit (sigmoid)</td></tr>
            <tr><td>Loss</td><td>BCEWithLogitsLoss</td></tr>
            <tr><td>Optimizer</td><td>Adam, lr=1e-3</td></tr>
            <tr><td>Epochs</td><td>10</td></tr>
            </table>"""
            + C.panel_close(),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            C.panel_open("Features used")
            + """<p style='color:#C8C3B8; font-size:0.9rem; line-height:1.7;'>
            merchant · category · amt · city · state · lat · long ·
            city_pop · job · merch_lat · merch_long
            </p>
            <p style='color:#8A8F9C; font-size:0.82rem;'>Dropped as identifiers/leakage: trans_date_trans_time, dob, trans_num.</p>"""
            + C.panel_close(),
            unsafe_allow_html=True,
        )

    st.markdown(
        C.panel_open("Tech stack")
        + "<div>"
        + " ".join([C.pill(x) for x in [
            "PyTorch", "scikit-learn", "pandas", "Streamlit", "OrdinalEncoder", "StandardScaler",
        ]])
        + "</div>" + C.panel_close(),
        unsafe_allow_html=True,
    )

    st.markdown(
        C.panel_open("Disclaimer")
        + "<p style='color:#8A8F9C; font-size:0.85rem;'>This model is a data-science portfolio project, "
          "not a certified fraud-detection system. Do not use it to make real financial or legal decisions.</p>"
        + C.panel_close(),
        unsafe_allow_html=True,
    )

    st.markdown(C.footer_note("FRAUD SENTINEL · BUILT WITH PYTORCH + STREAMLIT"), unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Router
# ----------------------------------------------------------------------------
if st.session_state.get("_nav_hint"):
    page = st.session_state.pop("_nav_hint")

if page == "Overview":
    page_overview()
elif page == "Predict":
    page_predict()
elif page == "Analytics":
    page_analytics()
elif page == "Model Performance":
    page_performance()
elif page == "About":
    page_about()
