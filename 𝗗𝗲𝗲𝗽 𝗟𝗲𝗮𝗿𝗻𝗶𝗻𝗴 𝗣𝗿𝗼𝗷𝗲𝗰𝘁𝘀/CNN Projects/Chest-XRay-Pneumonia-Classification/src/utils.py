"""Shared constants and small helpers used across the app."""

from __future__ import annotations

import os

import torch

# Project root = one level up from src/
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)

MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
GRAPHS_DIR = os.path.join(PROJECT_ROOT, "graphs")

# Filenames the app will look for, in this order of preference.
# The notebook (Cell 70) saves the first two names below; we also accept a
# simpler renamed pair so users can drop weights in without renaming.
MODEL_WEIGHT_CANDIDATES = [
    "xray_model.pth",
    "chest_xray_model.pth",
    "new_chest_xray_model_bht.pth",
]
CHECKPOINT_CANDIDATES = [
    "chest_xray_checkpoint.pth",
    "new_chest_xray_checkpoint_bht.pth",
]
CLASS_MAP_CANDIDATES = [
    "class_to_idx.json",
    "new_class_to_idx_bht.json",
]
METRICS_CANDIDATES = [
    "metrics.json",
]

# Default class mapping, matching torchvision's ImageFolder, which assigns
# indices in sorted() order of the subfolder names ("NORMAL", "PNEUMONIA").
# This is the standard, deterministic ImageFolder behavior -- not a guess --
# but it is overridden automatically if a class_to_idx.json is found.
DEFAULT_CLASS_TO_IDX = {"NORMAL": 0, "PNEUMONIA": 1}

APP_TITLE = "Chest X-Ray Classification"
DISCLAIMER = (
    "This application is an educational / research demonstration. It "
    "classifies the uploaded image based on patterns learned during "
    "training and is **not a medical diagnosis**. Predictions can be "
    "incorrect. Always consult a qualified medical professional for "
    "actual diagnosis or treatment decisions."
)


def get_device() -> torch.device:
    """Use CUDA if available, otherwise fall back to CPU. Never assume GPU."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def find_existing_file(directory: str, candidates: list[str]) -> str | None:
    """Return the full path of the first candidate filename that exists."""
    for name in candidates:
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            return path
    return None
