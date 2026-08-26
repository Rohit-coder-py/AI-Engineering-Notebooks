# ---------------------------------------------------------
# src/inference.py
# Handles model loading and prediction for new input data.
# ---------------------------------------------------------

import os
import torch

from src.model import OptunaShipSenseModel
from src.preprocessing import feature_order, best_hyperparameters, MODELS_DIR

MODEL_PATH = os.path.join(MODELS_DIR, "shipsense_model.pth")


def load_model() -> OptunaShipSenseModel:
    """Build the network with the tuned architecture and load trained weights."""
    net = OptunaShipSenseModel(
        input_features=len(feature_order),
        hidden1=best_hyperparameters["hidden1"],
        hidden2=best_hyperparameters["hidden2"],
        hidden3=best_hyperparameters["hidden3"],
        dropout=best_hyperparameters["dropout"],
    )
    state_dict = torch.load(MODEL_PATH, map_location="cpu")
    net.load_state_dict(state_dict)
    net.eval()  # turn off dropout -- deterministic inference
    return net


def predict_proba(model: OptunaShipSenseModel, scaled_input) -> float:
    """Run a forward pass on a pre-scaled input row and return P(late delivery)."""
    input_tensor = torch.tensor(scaled_input, dtype=torch.float32)
    with torch.no_grad():
        logit = model(input_tensor)
        probability = torch.sigmoid(logit).item()
    return probability


# Loaded once at import time (module-level singleton), same pattern the
# original app relied on. app.py wraps the *first* access to this module
# in st.cache_resource so Streamlit only pays this cost once per session.
model = load_model()
