"""
Loads the trained model + scaler + feature order once, and exposes a single
predict(raw_dict) function used by app/app.py.
"""

import os

import joblib
import numpy as np
import torch

from model import MyModel
from preprocessing import build_feature_row

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

_model = None
_scaler = None
_feature_order = None


def load_artifacts():
    """Loads model/scaler/feature_order into module-level singletons."""
    global _model, _scaler, _feature_order

    if _model is not None:
        return _model, _scaler, _feature_order

    _scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
    _feature_order = joblib.load(os.path.join(MODELS_DIR, "feature_order.pkl"))

    weights = np.load(os.path.join(MODELS_DIR, "churn_model_weights.npz"))
    _model = MyModel(n_features=len(_feature_order))
    state_dict = {k: torch.tensor(weights[k]) for k in weights.files}
    _model.load_state_dict(state_dict)
    _model.eval()

    return _model, _scaler, _feature_order


def predict(raw: dict) -> dict:
    """
    raw: dict of raw form values (see preprocessing.build_feature_row for
         the exact keys expected).
    Returns: {"churn_probability": float, "churn_prediction": 0/1}
    """
    model, scaler, feature_order = load_artifacts()

    row_df = build_feature_row(raw, feature_order)
    row_scaled = scaler.transform(row_df)
    row_tensor = torch.tensor(row_scaled, dtype=torch.float32)

    with torch.no_grad():
        logit = model(row_tensor)
        prob = torch.sigmoid(logit).item()

    return {
        "churn_probability": prob,
        "churn_prediction": int(prob >= 0.5),
    }
