"""
Inference helper used by the Streamlit app.

Loads the trained model + preprocessing artifacts once, and exposes a
`predict(df)` function that takes a raw-feature dataframe and returns
fraud probabilities + binary predictions.
"""

import os
import torch
import numpy as np
import pandas as pd

import sys
sys.path.append(os.path.dirname(__file__))

from model import load_model          # noqa: E402
from preprocessing import FraudPreprocessor  # noqa: E402


class FraudPredictor:
    def __init__(self, models_dir: str, threshold: float = 0.5):
        self.preprocessor = FraudPreprocessor(models_dir)
        n_features = len(self.preprocessor.feature_order)
        self.model = load_model(f"{models_dir}/fraud_model.pth", n_features=n_features)
        self.threshold = threshold

    def predict(self, df: pd.DataFrame, threshold: float | None = None):
        """
        df: dataframe with columns matching self.preprocessor.feature_order
        returns: (probabilities: np.ndarray, predictions: np.ndarray)
        """
        thresh = threshold if threshold is not None else self.threshold
        X_scaled = self.preprocessor.transform(df)
        X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
        with torch.no_grad():
            logits = self.model(X_tensor).squeeze(-1)
            probs = torch.sigmoid(logits).numpy()
        preds = (probs >= thresh).astype(int)
        return probs, preds
