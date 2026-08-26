# ---------------------------------------------------------
# app.py -- ShipSense: Late Delivery Risk Predictor
# Streamlit front-end. Run with:  streamlit run app.py
# ---------------------------------------------------------

import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.preprocessing import (
    scaler,
    encoder,
    feature_order,
    categorical_columns,
    best_hyperparameters,
)
from src.inference import model, predict_proba
from src.utils import risk_band, contributing_signals, load_dataset, dataset_summary

GRAPHS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphs")

# ---------------------------------------------------------
# Page config + light styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="ShipSense | Late Delivery Risk Predictor",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; }
    .ss-hero {
        background: linear-gradient(90deg, #0f172a 0%, #1e3a5f 100%);
        padding: 1.6rem 1.8rem; border-radius: 14px; color: #f8fafc; margin-bottom: 1.2rem;
    }
    .ss-hero h1 { margin: 0; font-size: 1.7rem; }
    .ss-hero p { margin: .3rem 0 0 0; opacity: .85; }
    .ss-card {
        border-radius: 14px; padding: 1.2rem 1.4rem; border: 1px solid rgba(120,120,120,.2);
        background: rgba(120,120,120,.04); margin-bottom: .8rem;
    }
    .ss-badge {
        display: inline-block; padding: .25rem .7rem; border-radius: 999px;
        font-weight: 600; font-size: .85rem; color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Cache expensive / repeated work
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_category_options():
    return {col: list(cats) for col, cats in zip(categorical_columns, encoder.categories_)}


@st.cache_data(show_spinner=False)
def get_dataset():
    return load_dataset()


category_options = get_category_options()

# ---------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 🚚 ShipSense")
    st.caption("AI-powered shipping delay intelligence")
    page = st.radio(
        "Navigate",
        ["🔮 Predict", "📊 Insights & EDA", "🧠 Model Info", "ℹ️ About"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Built with PyTorch + Streamlit")

# ---------------------------------------------------------
# Shared header
# ---------------------------------------------------------
st.markdown(
    """
    <div class="ss-hero">
        <h1>🚚 ShipSense — Late Delivery Risk Predictor</h1>
        <p>A deep learning system that predicts the probability a shipment will arrive late,
        so ops and logistics teams can intervene before it happens.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def build_gauge(probability: float, band: dict) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            number={"suffix": "%"},
            title={"text": "Predicted Late Delivery Probability"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": band["color"]},
                "steps": [
                    {"range": [0, 40], "color": "rgba(18,183,106,.18)"},
                    {"range": [40, 70], "color": "rgba(245,165,36,.18)"},
                    {"range": [70, 100], "color": "rgba(229,72,77,.18)"},
                ],
            },
        )
    )
    fig.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=10))
    return fig


# ===========================================================
# PAGE 1 — PREDICT
# ===========================================================
if page == "🔮 Predict":
    tab_single, tab_batch = st.tabs(["Single Shipment", "Batch (CSV) Prediction"])

    # -------------------- Single prediction --------------------
    with tab_single:
        with st.form("prediction_form"):
            c1, c2, c3 = st.columns(3)

            with c1:
                st.subheader("Order Details")
                Type = st.selectbox("Payment Type", category_options["Type"])
                Shipping_Mode = st.selectbox("Shipping Mode", category_options["Shipping Mode"])
                Days_scheduled = st.slider("Days for Shipment (Scheduled)", 0, 4, 3)
                Order_Item_Quantity = st.slider("Order Item Quantity", 1, 5, 2)

                st.subheader("Product / Category")
                Category_Name = st.selectbox("Category Name", category_options["Category Name"])
                Department_Name = st.selectbox("Department Name", category_options["Department Name"])
                Product_Price = st.number_input("Product Price ($)", value=141.0)
                Order_Item_Product_Price = st.number_input("Order Item Product Price ($)", value=141.0)
                Sales = st.number_input("Sales ($)", value=203.0)

            with c2:
                st.subheader("Discount & Profit")
                Order_Item_Discount = st.number_input("Order Item Discount ($)", value=20.0)
                Order_Item_Discount_Rate = st.slider("Order Item Discount Rate", 0.0, 0.25, 0.10)
                Order_Item_Profit_Ratio = st.number_input("Order Item Profit Ratio", value=0.12)
                Benefit_per_order = st.number_input("Benefit per Order ($)", value=22.0)
                Sales_per_customer = st.number_input("Sales per Customer ($)", value=183.0)
                Order_Item_Total = st.number_input("Order Item Total ($)", value=183.0)
                Order_Profit_Per_Order = st.number_input("Order Profit Per Order ($)", value=22.0)

                st.subheader("Customer Info")
                Customer_Segment = st.selectbox("Customer Segment", category_options["Customer Segment"])
                Customer_Country = st.selectbox("Customer Country", category_options["Customer Country"])
                Customer_State = st.selectbox("Customer State", sorted(category_options["Customer State"]))
                Customer_City = st.selectbox("Customer City", sorted(category_options["Customer City"]))

            with c3:
                st.subheader("Order Location")
                Market = st.selectbox("Market", category_options["Market"])
                Order_Region = st.selectbox("Order Region", category_options["Order Region"])
                Order_Country = st.selectbox("Order Country", sorted(category_options["Order Country"]))
                Order_State = st.selectbox("Order State", sorted(category_options["Order State"]))
                Order_City = st.selectbox("Order City", sorted(category_options["Order City"]))
                Latitude = st.number_input("Latitude", value=29.7, format="%.4f")
                Longitude = st.number_input("Longitude", value=-84.9, format="%.4f")

            submitted = st.form_submit_button("🔮 Predict Delay Risk", use_container_width=True)

        if submitted:
            input_dict = {
                "Type": Type,
                "Days for shipment (scheduled)": Days_scheduled,
                "Benefit per order": Benefit_per_order,
                "Sales per customer": Sales_per_customer,
                "Category Name": Category_Name,
                "Customer City": Customer_City,
                "Customer Country": Customer_Country,
                "Customer Segment": Customer_Segment,
                "Customer State": Customer_State,
                "Department Name": Department_Name,
                "Latitude": Latitude,
                "Longitude": Longitude,
                "Market": Market,
                "Order City": Order_City,
                "Order Country": Order_Country,
                "Order Item Discount": Order_Item_Discount,
                "Order Item Discount Rate": Order_Item_Discount_Rate,
                "Order Item Product Price": Order_Item_Product_Price,
                "Order Item Profit Ratio": Order_Item_Profit_Ratio,
                "Order Item Quantity": Order_Item_Quantity,
                "Sales": Sales,
                "Order Item Total": Order_Item_Total,
                "Order Profit Per Order": Order_Profit_Per_Order,
                "Order Region": Order_Region,
                "Order State": Order_State,
                "Product Price": Product_Price,
                "Shipping Mode": Shipping_Mode,
            }

            input_df = pd.DataFrame([input_dict])[feature_order]
            input_df[categorical_columns] = encoder.transform(input_df[categorical_columns])
            scaled_input = scaler.transform(input_df)
            probability = predict_proba(model, scaled_input)
            band = risk_band(probability)

            st.markdown("---")
            r1, r2 = st.columns([1, 1])
            with r1:
                st.markdown(
                    f"""
                    <div class="ss-card">
                        <span class="ss-badge" style="background:{band['color']}">
                            {band['emoji']} {band['label']}
                        </span>
                        <h2 style="margin:.6rem 0 0 0;">{probability:.1%} chance of late delivery</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.write("**Contributing signals:**")
                for s in contributing_signals(input_dict):
                    st.write(f"- {s}")
            with r2:
                st.plotly_chart(build_gauge(probability, band), use_container_width=True)

    # -------------------- Batch prediction --------------------
    with tab_batch:
        st.write(
            "Upload a CSV with the same columns as the training data "
            f"({len(feature_order)} feature columns) to score many shipments at once."
        )
        st.code(", ".join(feature_order), language="text")
        uploaded = st.file_uploader("Upload shipments CSV", type=["csv"])
        if uploaded is not None:
            try:
                batch_df = pd.read_csv(uploaded)
                missing = [c for c in feature_order if c not in batch_df.columns]
                if missing:
                    st.error(f"Missing required column(s): {', '.join(missing)}")
                else:
                    work_df = batch_df[feature_order].copy()
                    work_df[categorical_columns] = encoder.transform(work_df[categorical_columns])
                    scaled = scaler.transform(work_df)
                    probs = [predict_proba(model, scaled[i : i + 1]) for i in range(len(scaled))]
                    batch_df["late_delivery_probability"] = [round(p, 4) for p in probs]
                    batch_df["risk_label"] = [risk_band(p)["label"] for p in probs]
                    st.success(f"Scored {len(batch_df)} shipments.")
                    st.dataframe(batch_df, use_container_width=True)
                    st.download_button(
                        "⬇️ Download results as CSV",
                        batch_df.to_csv(index=False).encode("utf-8"),
                        file_name="shipsense_predictions.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
            except Exception as e:
                st.error(f"Couldn't process this file: {e}")

# ===========================================================
# PAGE 2 — INSIGHTS & EDA
# ===========================================================
elif page == "📊 Insights & EDA":
    df = get_dataset()
    stats = dataset_summary(df)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Training Rows", f"{stats['rows']:,}")
    m2.metric("Features", stats["features"])
    m3.metric("Late Deliveries", f"{stats['late_count']:,}")
    m4.metric("Late Delivery Rate", f"{stats['late_rate']:.1%}")

    st.markdown("### Exploratory Data Analysis")
    st.caption("Generated during training and bundled with the model for reference.")

    captions = {
        "01_target_distribution.png": "Class balance: on-time vs. late deliveries.",
        "02_shipping_mode_vs_risk.png": "Late delivery risk by shipping mode.",
        "03_scheduled_days_vs_risk.png": "Risk vs. scheduled shipment days.",
        "04_correlation_heatmap.png": "Correlation heatmap across numerical features.",
        "05_customer_segment_vs_risk.png": "Risk by customer segment.",
        "06_order_region_vs_risk.png": "Risk by order region.",
    }
    files = sorted(os.listdir(GRAPHS_DIR)) if os.path.isdir(GRAPHS_DIR) else []
    cols = st.columns(2)
    for i, fname in enumerate(files):
        with cols[i % 2]:
            st.image(os.path.join(GRAPHS_DIR, fname), caption=captions.get(fname, fname), use_container_width=True)

# ===========================================================
# PAGE 3 — MODEL INFO
# ===========================================================
elif page == "🧠 Model Info":
    st.markdown("### Architecture")
    st.write(
        "ShipSense uses a fully-connected feed-forward neural network (PyTorch), "
        "with hyperparameters tuned via **Optuna**."
    )
    hp1, hp2, hp3, hp4, hp5 = st.columns(5)
    hp1.metric("Input Features", len(feature_order))
    hp2.metric("Hidden Layer 1", best_hyperparameters["hidden1"])
    hp3.metric("Hidden Layer 2", best_hyperparameters["hidden2"])
    hp4.metric("Hidden Layer 3", best_hyperparameters["hidden3"])
    hp5.metric("Dropout", best_hyperparameters["dropout"])

    st.code(
        "Input -> Linear -> ReLU -> Dropout\n"
        "       -> Linear -> ReLU -> Dropout\n"
        "       -> Linear -> ReLU -> Dropout\n"
        "       -> Linear -> Sigmoid -> P(late delivery)",
        language="text",
    )

    st.markdown("### Preprocessing Pipeline")
    st.write(
        "1. **Ordinal encoding** on categorical fields "
        f"({len(categorical_columns)} columns)\n"
        "2. **Standard scaling** on the full feature row\n"
        "3. Forward pass through the trained network -> sigmoid -> probability"
    )

    with st.expander("Full feature list"):
        st.write(feature_order)

# ===========================================================
# PAGE 4 — ABOUT
# ===========================================================
else:
    st.markdown("### About ShipSense")
    st.write(
        "ShipSense is an end-to-end machine learning system that predicts whether a shipment "
        "is at risk of arriving late, using order, product, customer, and logistics attributes "
        "known at the time an order is placed."
    )

    st.markdown("### Use Cases")
    st.markdown(
        """
        | Use case | Who benefits |
        |---|---|
        | Flag high-risk orders at checkout for proactive customer communication | E-commerce / D2C ops |
        | Prioritize carrier or route changes for at-risk shipments | Logistics & fulfillment teams |
        | Feed risk scores into SLA / customer-support dashboards | Customer support |
        | Batch-score historical or incoming order feeds | Data & analytics teams |
        """
    )

    st.markdown("### Tech Stack")
    st.write("Python · PyTorch · scikit-learn · Streamlit · Plotly · Optuna (hyperparameter tuning)")
