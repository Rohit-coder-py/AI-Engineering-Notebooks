"""
Model loading and inference.

This module is deliberately honest about missing artifacts: if no trained
weights are found in models/, it raises ModelNotFoundError rather than
returning a fake prediction. The UI layer catches this and shows clear
setup instructions instead of a result.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import torch
import torch.nn.functional as F

from src.model import XRayModel
from src.utils import (
    CHECKPOINT_CANDIDATES,
    CLASS_MAP_CANDIDATES,
    DEFAULT_CLASS_TO_IDX,
    MODEL_WEIGHT_CANDIDATES,
    MODELS_DIR,
    find_existing_file,
    get_device,
)


class ModelNotFoundError(Exception):
    """Raised when no trained weight file can be located in models/."""


@dataclass
class PredictionResult:
    predicted_label: str
    confidence: float  # 0-100, for the predicted class
    class_probabilities: dict[str, float]  # label -> percentage (0-100)


def _resolve_weights_path() -> str:
    path = find_existing_file(MODELS_DIR, MODEL_WEIGHT_CANDIDATES)
    if path:
        return path
    path = find_existing_file(MODELS_DIR, CHECKPOINT_CANDIDATES)
    if path:
        return path
    raise ModelNotFoundError(
        "No trained model weights were found in the models/ folder.\n\n"
        f"Expected one of: {', '.join(MODEL_WEIGHT_CANDIDATES + CHECKPOINT_CANDIDATES)}.\n\n"
        "Export your trained weights from the notebook "
        "(torch.save(model.state_dict(), 'models/xray_model.pth')) and place "
        "the file in the models/ folder, then reload the app."
    )


def _load_class_to_idx() -> dict[str, int]:
    path = find_existing_file(MODELS_DIR, CLASS_MAP_CANDIDATES)
    if path is None:
        return DEFAULT_CLASS_TO_IDX
    with open(path, "r") as f:
        mapping = json.load(f)
    return {str(k): int(v) for k, v in mapping.items()}


def _extract_state_dict(checkpoint) -> dict:
    """Handle a plain state_dict, a {'model_state_dict': ...} checkpoint,
    or a whole pickled nn.Module (all three are produced by different
    torch.save calls people commonly use)."""
    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        return checkpoint["model_state_dict"]
    if isinstance(checkpoint, dict):
        return checkpoint
    if isinstance(checkpoint, torch.nn.Module):
        return checkpoint.state_dict()
    raise ModelNotFoundError(
        "The model file was found but its format wasn't recognized "
        "(expected a state_dict or a checkpoint dict)."
    )


class ModelBundle:
    """Holds everything needed to run inference: the model, device, and
    the index -> label mapping."""

    def __init__(self, model: XRayModel, device: torch.device, idx_to_label: dict[int, str]):
        self.model = model
        self.device = device
        self.idx_to_label = idx_to_label

    def predict(self, input_tensor: torch.Tensor) -> PredictionResult:
        input_tensor = input_tensor.to(self.device)
        with torch.no_grad():
            logits = self.model(input_tensor)
            probs = F.softmax(logits, dim=1).squeeze(0).cpu()

        percentages = {
            self.idx_to_label[i]: float(probs[i]) * 100.0 for i in range(len(probs))
        }
        predicted_idx = int(torch.argmax(probs).item())
        predicted_label = self.idx_to_label[predicted_idx]
        confidence = percentages[predicted_label]

        return PredictionResult(
            predicted_label=predicted_label,
            confidence=confidence,
            class_probabilities=percentages,
        )


def load_model_bundle() -> ModelBundle:
    """Load weights from disk and build a ready-to-use ModelBundle.

    Raises ModelNotFoundError if no weights are present. Callers should
    wrap this (it's cheap to call once and cache in the UI layer with
    st.cache_resource).
    """
    device = get_device()
    weights_path = _resolve_weights_path()
    class_to_idx = _load_class_to_idx()
    idx_to_label = {idx: label for label, idx in class_to_idx.items()}

    checkpoint = torch.load(weights_path, map_location=device, weights_only=False)
    state_dict = _extract_state_dict(checkpoint)

    model = XRayModel()
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    return ModelBundle(model=model, device=device, idx_to_label=idx_to_label)
