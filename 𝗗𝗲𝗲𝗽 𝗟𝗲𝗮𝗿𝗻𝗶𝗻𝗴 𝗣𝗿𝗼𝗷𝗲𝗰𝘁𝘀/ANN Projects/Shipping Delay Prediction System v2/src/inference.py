# inference.py
# Handles model loading and prediction for new input data.

import torch

from src.model import OptunaShipSenseModel
from src.preprocessing import feature_order, best_hyperparameters


model = OptunaShipSenseModel(
    input_features=len(feature_order),
    hidden1=best_hyperparameters["hidden1"],
    hidden2=best_hyperparameters["hidden2"],
    hidden3=best_hyperparameters["hidden3"],
    dropout=best_hyperparameters["dropout"],
)
 
state_dict = torch.load("models/shipsense_model.pth", map_location="cpu")
model.load_state_dict(state_dict)
model.eval()  # turns off dropout -- we want deterministic predictions
 