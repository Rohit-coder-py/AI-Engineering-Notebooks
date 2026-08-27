import os
import torch

from model import InsuranceANN
from preprocessing import load_artifacts, transform_single

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
MODEL_PATH = os.path.join(BASE_DIR, "models", "medical_insurance_ann.pth")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_model = None
_encoder = None
_scaler = None
_feature_meta = None


def _load_once():
    global _model, _encoder, _scaler, _feature_meta

    if _model is None:
        _encoder, _scaler, _feature_meta = load_artifacts(ARTIFACTS_DIR)

        _model = InsuranceANN(input_dim=len(_feature_meta["feature_order"]))
        _model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        _model.to(device)
        _model.eval()

    return _model, _encoder, _scaler, _feature_meta


def predict(raw_input: dict) -> float:
    model, encoder, scaler, feature_meta = _load_once()

    processed = transform_single(
        raw_input,
        encoder,
        scaler,
        feature_meta["categorical_columns"],
        feature_meta["numerical_columns"],
    )

    input_tensor = torch.tensor(processed, dtype=torch.float32).to(device)

    with torch.no_grad():
        prediction = model(input_tensor).cpu().numpy().flatten()[0]

    return float(prediction)
