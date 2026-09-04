"""
Loading utilities for models, vectorizers, and evaluation artifacts.

All paths are resolved relative to this file's location (via pathlib),
so the app works no matter what directory `streamlit run` is launched
from.
"""

import json
from pathlib import Path

import joblib
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

LABEL_ORDER = ["neutral", "good", "bad"]  # index 0, 1, 2 (fixed by training)

DISPLAY_META = {
    "neutral": {"emoji": "😐", "color": "#8b93a7", "text": "Neutral"},
    "good": {"emoji": "🙂", "color": "#22c55e", "text": "Positive"},
    "bad": {"emoji": "🙁", "color": "#ef4444", "text": "Negative"},
}


class ModelBundle:
    """Container for a (vectorizer, model) pair plus friendly metadata."""

    def __init__(self, key, display_name, vectorizer, model):
        self.key = key
        self.display_name = display_name
        self.vectorizer = vectorizer
        self.model = model

    def predict(self, cleaned_text: str):
        """Return (predicted_label, {label: probability})."""
        vec = self.vectorizer.transform([cleaned_text])
        pred_idx = int(self.model.predict(vec)[0])
        pred_label = LABEL_ORDER[pred_idx]

        probs = None
        if hasattr(self.model, "predict_proba"):
            raw = self.model.predict_proba(vec)[0]
            # model.classes_ gives the actual index->slot mapping
            probs = {
                LABEL_ORDER[int(cls)]: float(p)
                for cls, p in zip(self.model.classes_, raw)
            }
        return pred_label, probs


def _require(path: Path, kind: str):
    if not path.exists():
        raise FileNotFoundError(
            f"Required {kind} file not found at '{path}'. "
            f"Make sure the 'models/' folder was included alongside app.py."
        )
    return path


def load_label_mapping():
    path = _require(MODELS_DIR / "label_mapping.json", "label mapping")
    with open(path, "r") as f:
        raw = json.load(f)  # {"0": "neutral", "1": "good", "2": "bad"}
    return {int(k): v for k, v in raw.items()}


def load_bundle(kind: str) -> ModelBundle:
    """kind: 'bow' or 'tfidf'"""
    if kind == "bow":
        vec_path = _require(MODELS_DIR / "bow_vectorizer.pkl", "BoW vectorizer")
        model_path = _require(MODELS_DIR / "logistic_model_bow.pkl", "BoW model")
        display_name = "Logistic Regression + Bag-of-Words"
    elif kind == "tfidf":
        vec_path = _require(MODELS_DIR / "tfidf_vectorizer.pkl", "TF-IDF vectorizer")
        model_path = _require(MODELS_DIR / "logistic_model_tfidf.pkl", "TF-IDF model")
        display_name = "Logistic Regression + TF-IDF"
    else:
        raise ValueError(f"Unknown model kind: {kind}")

    vectorizer = joblib.load(vec_path)
    model = joblib.load(model_path)
    return ModelBundle(kind, display_name, vectorizer, model)


def load_eval_report():
    path = MODELS_DIR / "eval_report.json"
    if not path.exists():
        return None
    with open(path, "r") as f:
        return json.load(f)


def load_confusion_matrix():
    path = MODELS_DIR / "confusion_matrix.npy"
    if not path.exists():
        return None
    return np.load(path)


def data_file_path(name: str) -> Path:
    return DATA_DIR / name
