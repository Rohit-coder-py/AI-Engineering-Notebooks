"""
infer.py
========
Loads the trained model + preprocessing artifacts and exposes a single
`predict()` function that takes a raw user input dict and returns a
probability + label. Used by both the CLI demo and the Streamlit app.
"""

import os
import torch
import pandas as pd

from preprocessing import (
    CATEGORICAL_COLS, NUMERICAL_COLS, load_artifacts
)
from model import AddictionANN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(ROOT, "models")


def load_model():
    scaler, encoders, feature_order = load_artifacts(MODELS_DIR)
    ckpt = torch.load(
        os.path.join(MODELS_DIR, "addiction_model.pth"),
        map_location="cpu", weights_only=False
    )
    model = AddictionANN(
        input_dim=ckpt["input_dim"],
        hidden_dims=ckpt["hidden_dims"],
        dropout=ckpt["dropout"],
    )
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()
    return model, scaler, encoders, feature_order


def predict(raw_input: dict, model, scaler, encoders, feature_order) -> dict:
    """
    raw_input keys expected:
        age, daily_screen_time_hours, social_media_hours, gaming_hours,
        work_study_hours, sleep_hours, notifications_per_day,
        app_opens_per_day, weekend_screen_time,
        gender, stress_level, academic_work_impact
    """
    df = pd.DataFrame([raw_input])

    # One-hot encode using the exact training-time dummy columns
    for col in CATEGORICAL_COLS:
        dummies = pd.get_dummies(df[col], prefix=col, dtype="int64")
        for c in encoders[col]:
            if c not in dummies.columns:
                dummies[c] = 0
        dummies = dummies[encoders[col]]
        df = pd.concat([df.drop(columns=[col]), dummies], axis=1)

    df = df[feature_order]
    df[NUMERICAL_COLS] = scaler.transform(df[NUMERICAL_COLS])

    x = torch.tensor(df.values, dtype=torch.float32)
    with torch.no_grad():
        logit = model(x)
        prob = torch.sigmoid(logit).item()

    return {
        "probability": prob,
        "label": int(prob >= 0.5),
        "risk_tier": (
            "Low" if prob < 0.34 else "Moderate" if prob < 0.67 else "High"
        ),
    }
