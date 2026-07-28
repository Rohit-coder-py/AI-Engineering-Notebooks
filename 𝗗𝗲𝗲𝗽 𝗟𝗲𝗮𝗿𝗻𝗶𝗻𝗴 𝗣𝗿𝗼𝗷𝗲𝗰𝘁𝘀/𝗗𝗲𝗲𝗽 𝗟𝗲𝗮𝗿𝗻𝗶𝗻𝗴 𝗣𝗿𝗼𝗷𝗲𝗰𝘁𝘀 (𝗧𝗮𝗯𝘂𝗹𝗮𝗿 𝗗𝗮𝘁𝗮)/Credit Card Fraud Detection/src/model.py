"""
PyTorch model architecture for Credit Card Fraud Detection.

Mirrors the FraudDetectionModel defined in
`notebooks/Credit Card Fraud Detection.ipynb` exactly, so that saved
weights (`models/fraud_model.pth`) load correctly here and in the
Streamlit app.
"""

import torch
import torch.nn as nn


class FraudDetectionModel(nn.Module):
    """Feed-forward ANN: 11 input features -> 16 -> 8 -> 1 logit."""

    def __init__(self, n_features: int = 11):
        super().__init__()
        self.fc1 = nn.Linear(n_features, 16)
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x


def load_model(weights_path: str, n_features: int = 11) -> FraudDetectionModel:
    """Load a trained model in eval mode, ready for inference."""
    model = FraudDetectionModel(n_features=n_features)
    state_dict = torch.load(weights_path, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model
