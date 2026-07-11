"""
utils.py
--------
Loading, caching, and inference helpers for the Shipment Delay
Intelligence application. All paths are relative to the project root
so the app runs unmodified locally and on Streamlit Community Cloud.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import joblib
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"
GRAPH_DIR = ROOT / "graphs"

# Exact column order the model / scaler were fitted on
# (matches: df.drop(columns=["ID", "Gender", "Reached.on.Time_Y.N", "Customer_rating"]))
FEATURE_ORDER = [
    "Warehouse_block",
    "Mode_of_Shipment",
    "Customer_care_calls",
    "Cost_of_the_Product",
    "Prior_purchases",
    "Product_importance",
    "Discount_offered",
    "Weight_in_gms",
]

MODEL_FILES = {
    "model": MODEL_DIR / "shipping_delay_model.pkl",
    "scaler": MODEL_DIR / "scaler.pkl",
    "warehouse_encoder": MODEL_DIR / "warehouse_encoder.pkl",
    "shipment_encoder": MODEL_DIR / "shipment_encoder.pkl",
    "importance_encoder": MODEL_DIR / "importance_encoder.pkl",
}

DATA_CANDIDATES = [
    DATA_DIR / "cleaned.csv",
    DATA_DIR / "shipping_delay_cleaned.csv",
    DATA_DIR / "raw_data.csv",
    DATA_DIR / "encoded.csv",
]


# --------------------------------------------------------------------
# Artifact loading
# --------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_artifacts():
    """
    Loads the trained model, scaler, and label encoders.
    Returns a dict of artifacts; missing files are reported (not raised)
    so the rest of the app can still render informative UI.
    """
    artifacts, missing = {}, []
    for key, path in MODEL_FILES.items():
        if path.exists():
            try:
                artifacts[key] = joblib.load(path)
            except Exception as e:  # noqa: BLE001
                missing.append(f"{path.name} (failed to load: {e})")
        else:
            missing.append(path.name)
    return artifacts, missing


@st.cache_data(show_spinner=False)
def load_dataset():
    """Loads the first available project dataset for analytics/EDA views."""
    for path in DATA_CANDIDATES:
        if path.exists():
            try:
                df = pd.read_csv(path)
                return df, path.name
            except Exception:  # noqa: BLE001
                continue
    return None, None


def graph_path(filename):
    """Returns a graph asset path if it exists on disk, else None."""
    p = GRAPH_DIR / filename
    return p if p.exists() else None


def artifacts_ready(artifacts):
    required = ["model", "scaler", "warehouse_encoder", "shipment_encoder", "importance_encoder"]
    return all(k in artifacts for k in required)


# --------------------------------------------------------------------
# Inference
# --------------------------------------------------------------------
def encode_category(encoder, value, fallback=0):
    """Safely transforms a single categorical value with a fitted LabelEncoder."""
    try:
        return int(encoder.transform([value])[0])
    except Exception:  # noqa: BLE001
        return fallback


def build_feature_row(raw_inputs, artifacts):
    """
    Builds a single-row DataFrame in the exact column order the
    scaler/model were fitted on, encoding categoricals with the
    saved LabelEncoders.
    """
    warehouse_enc = encode_category(artifacts["warehouse_encoder"], raw_inputs["Warehouse_block"])
    shipment_enc = encode_category(artifacts["shipment_encoder"], raw_inputs["Mode_of_Shipment"])
    importance_enc = encode_category(artifacts["importance_encoder"], raw_inputs["Product_importance"])

    row = {
        "Warehouse_block": warehouse_enc,
        "Mode_of_Shipment": shipment_enc,
        "Customer_care_calls": raw_inputs["Customer_care_calls"],
        "Cost_of_the_Product": raw_inputs["Cost_of_the_Product"],
        "Prior_purchases": raw_inputs["Prior_purchases"],
        "Product_importance": importance_enc,
        "Discount_offered": raw_inputs["Discount_offered"],
        "Weight_in_gms": raw_inputs["Weight_in_gms"],
    }
    return pd.DataFrame([row], columns=FEATURE_ORDER)


def predict_delay(raw_inputs, artifacts):
    """
    Runs the full inference pipeline: encode -> scale -> predict.
    NOTE: the saved StackingClassifier was trained on the encoded model
    features (not the scaled ones -- see notebook cell [36]/[68]), so the
    model receives the encoded, unscaled feature row. The scaler is kept
    loaded and exposed for models/analytics that do require it.

    Returns dict with: label, is_delayed, probability (0-1 or None), raw_row
    """
    model = artifacts["model"]
    X_row = build_feature_row(raw_inputs, artifacts)

    pred = model.predict(X_row)[0]
    proba = None
    if hasattr(model, "predict_proba"):
        try:
            proba = float(model.predict_proba(X_row)[0][1])
        except Exception:  # noqa: BLE001
            proba = None

    return {
        "is_delayed": bool(pred == 1),
        "probability": proba,
        "raw_row": X_row,
    }


# --------------------------------------------------------------------
# Misc helpers
# --------------------------------------------------------------------
def fmt_pct(x, decimals=1):
    if x is None:
        return "N/A"
    return f"{x * 100:.{decimals}f}%"


CATEGORY_OPTIONS = {
    "Warehouse_block": ["A", "B", "C", "D", "F"],
    "Mode_of_Shipment": ["Flight", "Road", "Ship"],
    "Product_importance": ["low", "medium", "high"],
}
