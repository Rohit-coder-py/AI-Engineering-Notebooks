# ---------------------------------------------------------
# src/preprocessing.py
#
# Loads the fitted preprocessing artifacts produced during
# training (encoder, scaler, column order, etc.) and exposes
# a single function to turn a raw input dict into a model-ready,
# scaled numpy array using the exact same transform pipeline
# that was used when the model was trained.
#
# Pipeline:
#   raw input dict
#       -> single-row DataFrame (columns reordered to feature_order)
#       -> categorical columns encoded (fitted OrdinalEncoder, transform only)
#       -> full row scaled (fitted StandardScaler, transform only)
#       -> ready for torch.tensor(...)
# ---------------------------------------------------------

import os
import joblib

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")


def load_artifacts(models_dir: str = MODELS_DIR) -> dict:
    """Load every artifact saved at the end of training (joblib.dump)."""
    return {
        "scaler": joblib.load(os.path.join(models_dir, "scaler.pkl")),
        "encoder": joblib.load(os.path.join(models_dir, "encoder.pkl")),
        "feature_order": joblib.load(os.path.join(models_dir, "feature_order.pkl")),
        "categorical_columns": joblib.load(os.path.join(models_dir, "categorical_columns.pkl")),
        "numerical_columns": joblib.load(os.path.join(models_dir, "numerical_columns.pkl")),
        "best_hyperparameters": joblib.load(os.path.join(models_dir, "best_hyperparameters.pkl")),
    }


def preprocess_input(input_dict: dict, artifacts: dict):
    """
    Turn one raw input dict (values picked in the Streamlit form) into a
    scaled numpy array shaped exactly like the training data (X_train).
    """
    import pandas as pd

    feature_order = artifacts["feature_order"]
    categorical_columns = artifacts["categorical_columns"]
    encoder = artifacts["encoder"]
    scaler = artifacts["scaler"]

    df = pd.DataFrame([input_dict])[feature_order]
    df[categorical_columns] = encoder.transform(df[categorical_columns])
    return scaler.transform(df)


# ---------------------------------------------------------
# Module-level artifacts, loaded once at import time so the rest
# of the app (app.py, src/inference.py) can do a simple:
#   from src.preprocessing import scaler, encoder, feature_order, ...
# ---------------------------------------------------------
_artifacts = load_artifacts()

scaler = _artifacts["scaler"]
encoder = _artifacts["encoder"]
feature_order = _artifacts["feature_order"]
categorical_columns = _artifacts["categorical_columns"]
numerical_columns = _artifacts["numerical_columns"]
best_hyperparameters = _artifacts["best_hyperparameters"]
