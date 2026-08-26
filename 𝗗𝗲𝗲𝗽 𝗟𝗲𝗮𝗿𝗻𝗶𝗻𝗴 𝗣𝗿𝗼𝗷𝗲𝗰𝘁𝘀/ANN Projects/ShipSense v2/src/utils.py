# ---------------------------------------------------------
# src/utils.py
# Small, presentation-layer helpers used by app.py:
#   - risk banding / copy for a predicted probability
#   - a couple of quick, rule-of-thumb "why" signals for the result
#   - cached dataset stats for the Insights tab
# Kept separate from src/inference.py and src/preprocessing.py so the
# ML pipeline stays free of UI concerns.
# ---------------------------------------------------------

import os
import pandas as pd

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "shipment_dataset_cleaned.csv",
)


def risk_band(probability: float) -> dict:
    """Map a model probability to a label/color band for the UI."""
    if probability >= 0.70:
        return {"label": "High Risk", "color": "#e5484d", "emoji": "🔴"}
    if probability >= 0.40:
        return {"label": "Moderate Risk", "color": "#f5a524", "emoji": "🟠"}
    return {"label": "Low Risk", "color": "#12b76a", "emoji": "🟢"}


def contributing_signals(input_dict: dict) -> list:
    """
    Lightweight, human-readable heuristics that usually correlate with the
    dataset's late-delivery pattern. Not SHAP values -- just quick context
    to make the prediction feel less like a black box.
    """
    signals = []
    if input_dict.get("Shipping Mode") in ("Standard Class",):
        signals.append("Standard Class shipping tends to carry more delay risk than Express/First Class in this dataset.")
    if input_dict.get("Days for shipment (scheduled)", 0) <= 1:
        signals.append("A very tight scheduled shipment window leaves little slack for disruption.")
    if input_dict.get("Order Item Discount Rate", 0) >= 0.15:
        signals.append("High discount-rate orders show a mild correlation with delay risk in the training data.")
    if not signals:
        signals.append("No strong individual risk signal detected -- prediction is driven by the combined feature profile.")
    return signals


def load_dataset() -> pd.DataFrame:
    """Load the cleaned training dataset once (used only by the Insights tab)."""
    return pd.read_csv(DATA_PATH)


def dataset_summary(df: pd.DataFrame) -> dict:
    late = int(df["Late_delivery_risk"].sum())
    total = len(df)
    return {
        "rows": total,
        "features": df.shape[1] - 1,
        "late_count": late,
        "on_time_count": total - late,
        "late_rate": late / total,
    }
