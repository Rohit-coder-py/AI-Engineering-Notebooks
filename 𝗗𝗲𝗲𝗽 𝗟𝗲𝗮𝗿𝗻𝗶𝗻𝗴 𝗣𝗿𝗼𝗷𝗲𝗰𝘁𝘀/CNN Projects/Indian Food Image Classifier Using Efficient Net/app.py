"""
Indian Food Image Classifier — Streamlit inference application.

Serves the EfficientNet-B0 model that was fine-tuned in
`notebook/Indian_Food_Image_Classifier.ipynb`. The preprocessing pipeline and
model surgery reproduced here are identical to the notebook's `eval_transform`
and classifier head replacement, so the saved `state_dict` loads strictly.

Run with:  streamlit run app.py
"""

from __future__ import annotations

import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import streamlit as st
import torch
import torch.nn.functional as F
from PIL import Image, ImageOps, UnidentifiedImageError
from torchvision import models, transforms

# --------------------------------------------------------------------------- #
# Configuration — mirrors the notebook exactly. Do not change casually.
# --------------------------------------------------------------------------- #

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

# The notebook saves `efficientnet.state_dict()` to *_final.pth and the tracked
# best weights (falling back to the current model) to *_best.pth. The best
# checkpoint is the intended production artifact.
WEIGHTS_CANDIDATES: Tuple[Path, ...] = (
    MODELS_DIR / "efficientnet_b0_best.pth",
    MODELS_DIR / "efficientnet_b0_final.pth",
)

# Both mapping files carry the same ordering; the EfficientNet run wrote
# class_to_idx.json, the baseline run wrote indian_food_class_to_idx.json.
CLASS_MAP_CANDIDATES: Tuple[Path, ...] = (
    MODELS_DIR / "class_to_idx.json",
    MODELS_DIR / "indian_food_class_to_idx.json",
)

METRICS_PATH = MODELS_DIR / "efficientnet_metrics.json"

# Bundled one-click demo images, named `<class_label>.jpg`. Optional — the
# gallery simply hides itself if the directory is absent.
SAMPLES_DIR = BASE_DIR / "assets" / "samples"

DETAIL_FULL = "Full breakdown"
DETAIL_TOP = "Top prediction only"

IMG_SIZE = 224
NORM_MEAN = [0.485, 0.456, 0.406]
NORM_STD = [0.229, 0.224, 0.225]

ARCHITECTURE = "EfficientNet-B0"
ACCEPTED_TYPES = ["jpg", "jpeg", "png", "webp"]
LOW_CONFIDENCE_THRESHOLD = 0.60

DISPLAY_OVERRIDES: Dict[str, str] = {
    "biryani": "Biryani",
    "butter_chicken": "Butter Chicken",
    "gulab_jamun": "Gulab Jamun",
    "naan": "Naan",
    "palak_paneer": "Palak Paneer",
}

CLASS_EMOJI: Dict[str, str] = {
    "biryani": "🍛",
    "butter_chicken": "🍗",
    "gulab_jamun": "🍮",
    "naan": "🫓",
    "palak_paneer": "🥘",
}


def display_name(raw: str) -> str:
    """Turn a machine class label into a presentable food name."""
    return DISPLAY_OVERRIDES.get(raw, raw.replace("_", " ").title())


# --------------------------------------------------------------------------- #
# Artifact loading
# --------------------------------------------------------------------------- #


@dataclass
class Prediction:
    """One class probability, ready for display."""

    label: str
    display: str
    emoji: str
    probability: float


@dataclass
class Classifier:
    """A loaded model plus everything needed to interpret its output."""

    model: torch.nn.Module
    idx_to_class: List[str]
    device: torch.device
    weights_name: str
    transform: transforms.Compose

    @property
    def num_classes(self) -> int:
        return len(self.idx_to_class)


class ArtifactError(RuntimeError):
    """Raised when a required model artifact is missing or unreadable."""


def _first_existing(candidates: Tuple[Path, ...], description: str) -> Path:
    for path in candidates:
        if path.is_file():
            return path
    names = ", ".join(f"models/{p.name}" for p in candidates)
    raise ArtifactError(f"No {description} found. Expected one of: {names}")


def load_class_mapping() -> List[str]:
    """Read class_to_idx and invert it into an index-ordered label list."""
    path = _first_existing(CLASS_MAP_CANDIDATES, "class mapping file")
    try:
        class_to_idx: Dict[str, int] = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ArtifactError(f"Class mapping {path.name} is not valid JSON.") from exc

    if not class_to_idx:
        raise ArtifactError(f"Class mapping {path.name} is empty.")

    indices = sorted(class_to_idx.values())
    if indices != list(range(len(class_to_idx))):
        raise ArtifactError(
            f"Class mapping {path.name} must map to contiguous indices 0..N-1."
        )

    ordered = [""] * len(class_to_idx)
    for label, idx in class_to_idx.items():
        ordered[idx] = label
    return ordered


def load_metrics() -> Dict[str, object]:
    """Training metrics are informational only; absence must not break the app."""
    if not METRICS_PATH.is_file():
        return {}
    try:
        return json.loads(METRICS_PATH.read_text())
    except json.JSONDecodeError:
        return {}


def build_model(num_classes: int) -> torch.nn.Module:
    """Recreate the notebook architecture: EfficientNet-B0 with a 5-way head."""
    model = models.efficientnet_b0(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier[1] = torch.nn.Linear(in_features, num_classes)
    return model


def build_transform() -> transforms.Compose:
    """The notebook's `eval_transform`, reproduced verbatim."""
    return transforms.Compose(
        [
            transforms.Resize((IMG_SIZE, IMG_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=NORM_MEAN, std=NORM_STD),
        ]
    )


@st.cache_resource(show_spinner=False)
def load_classifier() -> Classifier:
    """Load weights once per session and keep the model warm in memory."""
    idx_to_class = load_class_mapping()
    weights_path = _first_existing(WEIGHTS_CANDIDATES, "model weights file")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = build_model(len(idx_to_class))
    try:
        state = torch.load(weights_path, map_location="cpu")
    except Exception as exc:  # noqa: BLE001 — surfaced as a clean Streamlit error
        raise ArtifactError(f"Could not read {weights_path.name}: {exc}") from exc

    # Tolerate a full training checkpoint as well as a bare state_dict.
    if isinstance(state, dict) and "model_state_dict" in state:
        state = state["model_state_dict"]
    if not isinstance(state, dict):
        raise ArtifactError(f"{weights_path.name} does not contain a state_dict.")

    try:
        model.load_state_dict(state, strict=True)
    except RuntimeError as exc:
        raise ArtifactError(
            f"{weights_path.name} does not match the {ARCHITECTURE} architecture "
            f"with {len(idx_to_class)} output classes."
        ) from exc

    model.eval()
    model.to(device)

    return Classifier(
        model=model,
        idx_to_class=idx_to_class,
        device=device,
        weights_name=weights_path.name,
        transform=build_transform(),
    )


# --------------------------------------------------------------------------- #
# Inference
# --------------------------------------------------------------------------- #


def open_image(raw_bytes: bytes) -> Image.Image:
    """Decode uploaded bytes into an upright RGB image."""
    try:
        image = Image.open(io.BytesIO(raw_bytes))
        image.load()
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(
            "That file could not be read as an image. Please upload a valid "
            "JPG, JPEG, PNG or WEBP file."
        ) from exc
    return ImageOps.exif_transpose(image).convert("RGB")


@torch.no_grad()
def predict(clf: Classifier, image: Image.Image) -> List[Prediction]:
    """Run a single forward pass and return probabilities, highest first."""
    tensor = clf.transform(image).unsqueeze(0).to(clf.device)
    logits = clf.model(tensor)
    probs = F.softmax(logits, dim=1)[0].cpu().tolist()

    results = [
        Prediction(
            label=label,
            display=display_name(label),
            emoji=CLASS_EMOJI.get(label, "🍽️"),
            probability=float(prob),
        )
        for label, prob in zip(clf.idx_to_class, probs)
    ]
    return sorted(results, key=lambda r: r.probability, reverse=True)


# --------------------------------------------------------------------------- #
# Presentation
# --------------------------------------------------------------------------- #

CUSTOM_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

  :root {
    --ink:      #14110f;
    --panel:    #ffffff;
    --line:     #e7e1d8;
    --muted:    #6f665c;
    --accent:   #c2410c;
    --accent-2: #f59e0b;
  }

  .block-container { padding-top: 2.2rem; max-width: 1180px; }

  html, body, [class*="css"] { font-family: 'Inter', system-ui, sans-serif; }
  h1, h2, h3, h4 { font-family: 'Sora', 'Inter', sans-serif; letter-spacing: -0.02em; }

  /* Hero */
  .hero {
    position: relative;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 2.4rem 2.6rem;
    background:
      radial-gradient(120% 140% at 100% 0%, #fff2e2 0%, rgba(255,255,255,0) 55%),
      linear-gradient(180deg, #fffdfa 0%, #fdf8f2 100%);
    box-shadow: 0 1px 2px rgba(20,17,15,.04), 0 18px 40px -28px rgba(20,17,15,.28);
    overflow: hidden;
  }
  .hero::after {
    content: ""; position: absolute; inset: 0 0 auto 0; height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent-2), transparent);
  }
  .hero-eyebrow {
    display: inline-block; font-size: .72rem; font-weight: 600;
    letter-spacing: .16em; text-transform: uppercase; color: var(--accent);
    border: 1px solid #f3d3b6; background: #fff7ee;
    padding: .3rem .7rem; border-radius: 999px; margin-bottom: 1rem;
  }
  .hero h1 { font-size: 2.5rem; line-height: 1.1; margin: 0 0 .6rem; color: var(--ink); }
  .hero p  { font-size: 1.03rem; color: var(--muted); margin: 0; max-width: 46rem; }

  .stat-row { display: flex; flex-wrap: wrap; gap: 2.6rem; margin-top: 1.9rem; }
  .stat-k { font-family: 'Sora', sans-serif; font-size: 1.5rem; font-weight: 700; color: var(--ink); }
  .stat-l { font-size: .74rem; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin-top: .15rem; }

  /* Cards */
  .card {
    border: 1px solid var(--line); border-radius: 16px; background: var(--panel);
    padding: 1.5rem 1.7rem; box-shadow: 0 1px 2px rgba(20,17,15,.04);
    transition: box-shadow .25s ease, transform .25s ease;
  }
  .card:hover { box-shadow: 0 14px 34px -24px rgba(20,17,15,.35); }

  .section-title {
    font-family: 'Sora', sans-serif; font-size: .78rem; font-weight: 600;
    letter-spacing: .14em; text-transform: uppercase; color: var(--muted);
    margin: 2rem 0 .9rem; display: flex; align-items: center; gap: .8rem;
  }
  .section-title::after { content: ""; flex: 1; height: 1px; background: var(--line); }

  /* Result */
  .result {
    border: 1px solid #f0d9c4; border-radius: 18px; padding: 1.8rem 2rem;
    background: linear-gradient(135deg, #fffaf4 0%, #fff4e8 100%);
    animation: rise .45s cubic-bezier(.22,1,.36,1) both;
  }
  @keyframes rise { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
  .result-label { font-size: .74rem; letter-spacing: .14em; text-transform: uppercase; color: var(--accent); font-weight: 600; }
  .result-name { font-family: 'Sora', sans-serif; font-size: 2.15rem; font-weight: 700; color: var(--ink); margin: .35rem 0 .1rem; }
  .result-conf { font-size: 1.02rem; color: var(--muted); }
  .result-conf b { color: var(--ink); }

  /* Probability bars */
  .bar-row { margin-bottom: .95rem; }
  .bar-head { display: flex; justify-content: space-between; font-size: .9rem; margin-bottom: .35rem; }
  .bar-head .n { color: var(--ink); font-weight: 500; }
  .bar-head .v { color: var(--muted); font-variant-numeric: tabular-nums; }
  .bar-track { height: 9px; border-radius: 999px; background: #f1ece5; overflow: hidden; }
  .bar-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    animation: grow .7s cubic-bezier(.22,1,.36,1) both;
  }
  .bar-fill.dim { background: #cfc7bd; }
  @keyframes grow { from { width: 0 !important; } }

  /* Detail table */
  .kv { display: flex; justify-content: space-between; gap: 1rem;
        padding: .68rem 0; border-bottom: 1px dashed var(--line); font-size: .92rem; }
  .kv:last-child { border-bottom: none; }
  .kv span:first-child { color: var(--muted); }
  .kv span:last-child { color: var(--ink); font-weight: 500; }

  /* Empty upload prompt */
  .empty {
    border: 1.5px dashed var(--line); border-radius: 16px; padding: 3rem 2rem;
    text-align: center; color: var(--muted); background: #fdfbf8;
  }
  .empty .big { font-size: 1.7rem; margin-bottom: .6rem; }

  /* Sidebar */
  section[data-testid="stSidebar"] { background: #fdfbf8; border-right: 1px solid var(--line); }
  .side-h { font-family: 'Sora', sans-serif; font-size: .74rem; font-weight: 600;
            letter-spacing: .14em; text-transform: uppercase; color: var(--muted);
            margin: 1.4rem 0 .6rem; }
  .chip { display: inline-block; padding: .3rem .7rem; margin: 0 .3rem .4rem 0;
          border: 1px solid var(--line); border-radius: 999px; background: #fff;
          font-size: .84rem; color: var(--ink); }
  .device { display: inline-flex; align-items: center; gap: .45rem;
            font-size: .86rem; color: var(--ink); font-weight: 500; }
  .dot { width: 7px; height: 7px; border-radius: 50%; background: #16a34a; }

  [data-testid="stFileUploaderDropzone"] { border-radius: 14px; border-style: dashed; }
  [data-testid="stImage"] img { border-radius: 12px; }

  /* Sample gallery */
  .gallery-hint { font-size: .86rem; color: var(--muted); margin: -.2rem 0 .8rem; }
  [data-testid="stImage"] img:hover { filter: saturate(1.06); }
  div[data-testid="column"] .stButton > button {
    border-radius: 999px; border: 1px solid var(--line); background: #fff;
    font-size: .84rem; padding: .3rem .6rem; color: var(--ink);
    transition: border-color .2s ease, color .2s ease, background-color .2s ease;
  }
  div[data-testid="column"] .stButton > button:hover {
    border-color: var(--accent); color: var(--accent); background: #fff7ee;
  }
  footer, #MainMenu { visibility: hidden; }
</style>
"""


def bar(name: str, value: float, top: bool) -> str:
    pct = value * 100
    return (
        f'<div class="bar-row" data-testid="prob-row-{name.lower().replace(" ", "-")}">'
        f'<div class="bar-head"><span class="n">{name}</span>'
        f'<span class="v">{pct:.1f}%</span></div>'
        f'<div class="bar-track"><div class="bar-fill{"" if top else " dim"}" '
        f'style="width:{max(pct, 0.6):.2f}%"></div></div></div>'
    )


def render_hero(metrics: Dict[str, object], num_classes: int) -> None:
    accuracy = metrics.get("test_accuracy")
    accuracy_text = f"{accuracy}%" if accuracy is not None else "—"
    samples = metrics.get("test_samples", "—")
    st.markdown(
        f"""
        <div class="hero" data-testid="hero-section">
          <span class="hero-eyebrow">Computer Vision · Transfer Learning</span>
          <h1>Indian Food Image Classifier</h1>
          <p>AI-powered Indian food recognition using {ARCHITECTURE}. Upload a dish
             photograph and the model returns the predicted category along with its
             confidence score across all supported classes.</p>
          <div class="stat-row">
            <div><div class="stat-k">{ARCHITECTURE}</div><div class="stat-l">Architecture</div></div>
            <div><div class="stat-k">{accuracy_text}</div><div class="stat-l">Test Accuracy</div></div>
            <div><div class="stat-k">{num_classes}</div><div class="stat-l">Food Classes</div></div>
            <div><div class="stat-k">{samples}</div><div class="stat-l">Test Samples</div></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(clf: Classifier, metrics: Dict[str, object]) -> None:
    accuracy = metrics.get("test_accuracy")
    with st.sidebar:
        st.markdown('<div class="side-h">About the Model</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="kv"><span>Architecture</span><span>{ARCHITECTURE}</span></div>'
            f'<div class="kv"><span>Task</span><span>Image Classification</span></div>'
            f'<div class="kv"><span>Classes</span><span>{clf.num_classes}</span></div>'
            f'<div class="kv"><span>Test Accuracy</span>'
            f'<span>{f"{accuracy}%" if accuracy is not None else "—"}</span></div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="side-h">Supported Foods</div>', unsafe_allow_html=True)
        st.markdown(
            "".join(
                f'<span class="chip">{CLASS_EMOJI.get(c, "🍽️")} {display_name(c)}</span>'
                for c in clf.idx_to_class
            ),
            unsafe_allow_html=True,
        )

        st.markdown('<div class="side-h">Runtime</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="device" data-testid="device-indicator"><span class="dot"></span>'
            f"{clf.device.type.upper()}</div>",
            unsafe_allow_html=True,
        )
        st.caption(f"Weights · {clf.weights_name}")
        st.caption("Inference runs locally in `torch.no_grad()` mode.")


def render_results(
    clf: Classifier, results: List[Prediction], show_all: bool = True
) -> None:
    best = results[0]
    st.markdown(
        f"""
        <div class="result" data-testid="prediction-result">
          <div class="result-label">Prediction Result</div>
          <div class="result-name" data-testid="predicted-class">
            {best.emoji} {best.display}
          </div>
          <div class="result-conf" data-testid="prediction-confidence">
            <b>{best.probability * 100:.1f}%</b> confidence
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if best.probability < LOW_CONFIDENCE_THRESHOLD:
        st.warning(
            "The model is not highly confident in this prediction. The image may "
            "not belong to one of the supported food categories.",
            icon="⚠️",
        )

    if show_all:
        st.markdown(
            '<div class="section-title">All Class Probabilities</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="card" data-testid="probability-distribution">'
            + "".join(
                bar(f"{r.emoji} {r.display}", r.probability, i == 0)
                for i, r in enumerate(results)
            )
            + "</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title">Prediction Details</div>', unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="card" data-testid="prediction-details">'
        f'<div class="kv"><span>Predicted Food</span><span>{best.display}</span></div>'
        f'<div class="kv"><span>Confidence</span>'
        f"<span>{best.probability * 100:.2f}%</span></div>"
        f'<div class="kv"><span>Runner-up</span>'
        f"<span>{results[1].display} · {results[1].probability * 100:.2f}%</span></div>"
        f'<div class="kv"><span>Model</span><span>{ARCHITECTURE}</span></div>'
        f'<div class="kv"><span>Classes</span><span>{clf.num_classes}</span></div>'
        f'<div class="kv"><span>Input Resolution</span>'
        f"<span>{IMG_SIZE} × {IMG_SIZE}</span></div>"
        f'<div class="kv"><span>Inference Device</span>'
        f"<span>{clf.device.type.upper()}</span></div>"
        f"</div>",
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------- #
# App
# --------------------------------------------------------------------------- #


def available_samples(clf: Classifier) -> List[Tuple[str, Path]]:
    """Bundled demo images that exist on disk, in trained class order."""
    return [
        (label, SAMPLES_DIR / f"{label}.jpg")
        for label in clf.idx_to_class
        if (SAMPLES_DIR / f"{label}.jpg").is_file()
    ]


def render_gallery(clf: Classifier) -> None:
    """One-click example dishes so a visitor can try the model instantly."""
    samples = available_samples(clf)
    if not samples:
        return

    st.markdown(
        '<div class="section-title">Or Try a Sample Dish</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="gallery-hint" data-testid="gallery-hint">'
        "Pick any example below to run the classifier without uploading a file."
        "</div>",
        unsafe_allow_html=True,
    )

    for column, (label, path) in zip(st.columns(len(samples)), samples):
        with column:
            st.image(str(path), use_container_width=True)
            if st.button(
                display_name(label),
                key=f"sample-{label}",
                use_container_width=True,
            ):
                st.session_state["sample_choice"] = label


def resolve_source(upload: object | None) -> Tuple[str, bytes] | None:
    """An explicitly chosen sample wins; otherwise fall back to the upload."""
    choice = st.session_state.get("sample_choice")
    if choice:
        path = SAMPLES_DIR / f"{choice}.jpg"
        if path.is_file():
            return f"Sample · {display_name(choice)}", path.read_bytes()
        st.session_state["sample_choice"] = None

    if upload is not None:
        return upload.name, upload.getvalue()  # type: ignore[attr-defined]
    return None


def main() -> None:
    st.set_page_config(
        page_title="Indian Food Image Classifier",
        page_icon="🍛",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    metrics = load_metrics()

    try:
        clf = load_classifier()
    except ArtifactError as exc:
        render_hero(metrics, int(metrics.get("num_classes", 5) or 5))
        st.error(f"The classifier could not be initialised. {exc}", icon="🚫")
        st.info(
            "Ensure the `models/` directory contains the trained weights and the "
            "class mapping produced by the training notebook.",
            icon="ℹ️",
        )
        return

    render_hero(metrics, clf.num_classes)
    render_sidebar(clf, metrics)

    st.markdown(
        '<div class="section-title">Upload a Dish Photograph</div>',
        unsafe_allow_html=True,
    )

    upload = st.file_uploader(
        "Supported formats: JPG, JPEG, PNG, WEBP",
        type=ACCEPTED_TYPES,
        accept_multiple_files=False,
        key="food-image-uploader",
    )

    # A brand-new upload always supersedes a previously chosen sample dish.
    upload_id = f"{upload.name}:{upload.size}" if upload is not None else None
    if upload_id != st.session_state.get("last_upload_id"):
        st.session_state["last_upload_id"] = upload_id
        if upload_id is not None:
            st.session_state["sample_choice"] = None

    render_gallery(clf)

    source = resolve_source(upload)
    left, right = st.columns([1, 1.15], gap="large")

    if source is None:
        with left:
            st.markdown(
                '<div class="empty" data-testid="upload-placeholder">'
                '<div class="big">🍽️</div>'
                "<div>Upload an image or pick a sample to run the classifier.</div>"
                "<div style='font-size:.85rem;margin-top:.4rem'>"
                "Best results come from a clear, well-lit photo of a single dish."
                "</div></div>",
                unsafe_allow_html=True,
            )
        with right:
            st.markdown(
                '<div class="empty" data-testid="results-placeholder">'
                '<div class="big">📊</div>'
                "<div>Prediction and probability distribution appear here.</div>"
                "</div>",
                unsafe_allow_html=True,
            )
        return

    source_name, raw_bytes = source

    try:
        image = open_image(raw_bytes)
    except ValueError as exc:
        st.error(str(exc), icon="🖼️")
        return

    with left:
        st.markdown(
            '<div class="section-title" style="margin-top:0">Input Image</div>',
            unsafe_allow_html=True,
        )
        st.image(image, use_container_width=True)
        st.caption(
            f"{source_name} · {image.width} × {image.height} px · "
            f"resized to {IMG_SIZE} × {IMG_SIZE} for inference"
        )

    with right:
        detail_mode = st.radio(
            "Result detail",
            options=[DETAIL_FULL, DETAIL_TOP],
            horizontal=True,
            key="detail-mode",
        )

        try:
            with st.spinner("Analysing image…"):
                results = predict(clf, image)
        except Exception:  # noqa: BLE001 — never leak a traceback to the user
            st.error(
                "Inference failed for this image. Please try a different file.",
                icon="🚫",
            )
            return
        render_results(clf, results, show_all=detail_mode == DETAIL_FULL)

    st.markdown(
        '<div class="section-title">Limitations</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="card" data-testid="limitations-note">'
        f"This model was trained on only <b>{clf.num_classes}</b> Indian food "
        "categories. It has no notion of an <i>unknown</i> class, so any image "
        "outside those categories will still be mapped to the closest one it "
        "knows. Treat low-confidence results as inconclusive rather than correct."
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
