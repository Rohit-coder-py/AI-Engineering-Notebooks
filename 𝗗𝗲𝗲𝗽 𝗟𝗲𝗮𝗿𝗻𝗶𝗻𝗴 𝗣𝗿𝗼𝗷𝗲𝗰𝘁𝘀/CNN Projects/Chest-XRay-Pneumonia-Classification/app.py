"""
Chest X-Ray Classification -- single-file Streamlit app.

Run with: streamlit run app.py

Everything (Home, Classifier, Model Insights, About) lives in this one
file as tabs, so there's no pages/ multipage navigation to worry about.
"""

import json

import streamlit as st

from src.model import XRayModel
from src.prediction import ModelNotFoundError, load_model_bundle
from src.preprocessing import InvalidImageError, load_image, preprocess
from src.styles import (
    card_close,
    card_open,
    disclaimer_banner,
    hero,
    inject_global_css,
    pill_row,
    probability_bars,
    result_banner,
    status_badge,
    workflow,
)
from src.utils import APP_TITLE, DISCLAIMER, METRICS_CANDIDATES, MODELS_DIR, find_existing_file, get_device

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🩻",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()


@st.cache_resource(show_spinner="Loading model...")
def get_model_bundle():
    return load_model_bundle()


model_ready = True
load_error = None
try:
    get_model_bundle()
except ModelNotFoundError as exc:
    model_ready = False
    load_error = exc

with st.sidebar:
    st.markdown("### 🩻 Chest X-Ray AI")
    st.caption("Deep learning · Computer vision · PyTorch")
    status_badge(model_ready)
    st.markdown("---")
    st.caption(f"Compute: **{get_device().type.upper()}**")

tab_home, tab_classifier, tab_insights, tab_about = st.tabs(
    ["🏠 Home", "🔬 Classifier", "📊 Model Insights", "ℹ️ About"]
)

# =========================================================================
# HOME
# =========================================================================
with tab_home:
    hero(
        "Chest X-Ray Classification",
        "AI-powered chest X-ray image classification using a custom "
        "convolutional neural network, trained end-to-end to distinguish "
        "NORMAL from PNEUMONIA chest radiographs.",
    )

    col_cta, col_status = st.columns([1, 3])
    with col_cta:
        st.markdown(
            '<p class="xr-muted">👉 Head to the <b>🔬 Classifier</b> tab above '
            "to try it out.</p>",
            unsafe_allow_html=True,
        )
    with col_status:
        status_badge(model_ready)

    st.write("")
    st.subheader("Project overview")

    cols = st.columns(5)
    overview_items = [
        ("Deep Learning", "Custom CNN trained end-to-end"),
        ("Computer Vision", "Grayscale radiograph analysis"),
        ("X-Ray Classification", "NORMAL vs PNEUMONIA"),
        ("PyTorch", "Model, training & inference"),
        ("CNN", "4 conv blocks + FC head"),
    ]
    for col, (title, desc) in zip(cols, overview_items):
        with col:
            card_open()
            st.markdown(f"**{title}**")
            st.markdown(f'<p class="xr-muted">{desc}</p>', unsafe_allow_html=True)
            card_close()

    st.write("")
    st.subheader("How it works")
    workflow(
        [
            "Upload X-Ray",
            "Preprocessing",
            "Deep Learning Model",
            "Prediction",
            "Confidence",
        ]
    )

    st.write("")
    disclaimer_banner(DISCLAIMER)

# =========================================================================
# CLASSIFIER
# =========================================================================
with tab_classifier:
    hero(
        "X-Ray Classifier",
        "Upload a chest X-ray image (JPG or PNG) and the model will classify "
        "it as NORMAL or PNEUMONIA, along with a confidence score.",
    )

    if not model_ready:
        card_open("Setup required")
        st.error(str(load_error))
        card_close()

    left, right = st.columns([1, 1], gap="large")

    with left:
        card_open("Upload")
        uploaded_file = st.file_uploader(
            "Drop a chest X-ray image here, or click to browse",
            type=["jpg", "jpeg", "png"],
            disabled=not model_ready,
            key="classifier_upload",
        )

        image = None
        if uploaded_file is not None:
            try:
                image = load_image(uploaded_file.getvalue())
                st.image(image, caption="Uploaded X-ray", use_container_width=True)
            except InvalidImageError as exc:
                st.error(str(exc))
        else:
            st.markdown(
                '<p class="xr-muted">No image uploaded yet. Accepted formats: '
                "JPG, JPEG, PNG.</p>",
                unsafe_allow_html=True,
            )
        card_close()

    with right:
        card_open("Result")
        if not model_ready:
            st.markdown(
                '<p class="xr-muted">The classifier will appear here once a '
                "trained model is available.</p>",
                unsafe_allow_html=True,
            )
        elif image is None:
            st.markdown(
                '<p class="xr-muted">Upload an X-ray on the left to see the '
                "prediction, confidence, and full probability breakdown here.</p>",
                unsafe_allow_html=True,
            )
        else:
            try:
                with st.spinner("Running inference..."):
                    input_tensor = preprocess(image)
                    result = get_model_bundle().predict(input_tensor)
            except Exception as exc:  # unexpected inference failure
                st.error(
                    "Something went wrong while classifying this image. "
                    "Please try a different file."
                )
                st.caption(f"Technical detail: {exc}")
            else:
                result_banner(result.predicted_label, result.confidence)
                st.markdown("**Class probabilities**")
                probability_bars(result.class_probabilities)
        card_close()

    st.write("")
    disclaimer_banner(DISCLAIMER)

# =========================================================================
# MODEL INSIGHTS
# =========================================================================
with tab_insights:
    hero(
        "Model Insights",
        "A look under the hood: the network architecture, how it was trained, "
        "and its measured performance.",
    )

    card_open("Architecture")
    st.markdown(
        "The classifier is a **custom convolutional neural network** (no "
        "pretrained backbone) with four convolutional blocks followed by a "
        "global-average-pool and a fully-connected head:"
    )
    st.markdown(
        """
- **Conv Block 1** — Conv2d(1→32, 3×3) → ReLU → MaxPool
- **Conv Block 2** — Conv2d(32→64, 3×3) → ReLU → MaxPool
- **Conv Block 3** — Conv2d(64→128, 3×3) → ReLU → MaxPool
- **Conv Block 4** — Conv2d(128→256, 3×3) → ReLU → MaxPool
- **Global Average Pool** → 4×4 spatial output (handles any input size)
- **Fully Connected** — 4096 → 512 → 128 → 2 (ReLU between layers)
"""
    )

    param_count = sum(p.numel() for p in XRayModel().parameters())
    c1, c2, c3 = st.columns(3)
    c1.metric("Trainable parameters", f"{param_count:,}")
    c2.metric("Input size", "96 × 96 (grayscale)")
    c3.metric("Output classes", "2")
    card_close()

    col_in, col_out = st.columns(2)
    with col_in:
        card_open("Input")
        st.markdown(
            "A single-channel (grayscale) chest X-ray image, resized to "
            "96×96 and normalized with mean = 0.5, std = 0.5 — matching "
            "the exact preprocessing used during training."
        )
        card_close()
    with col_out:
        card_open("Output")
        st.markdown(
            "A 2-way classification: **NORMAL** or **PNEUMONIA**, "
            "returned as a softmax probability distribution over the "
            "two classes."
        )
        card_close()

    card_open("Training configuration")
    st.markdown("Configuration used in the training notebook:")
    pill_row(
        [
            "Loss: CrossEntropyLoss",
            "Optimizer: Adam (lr=0.001)",
            "Epochs: 12",
            "Batch size: 64",
            "Split: 70% / 15% / 15% (train/val/test)",
        ]
    )
    card_close()

    card_open("Performance")
    metrics_path = find_existing_file(MODELS_DIR, METRICS_CANDIDATES)

    if metrics_path is None:
        st.info(
            "No evaluation metrics file was found yet, so none are shown here "
            "— this app never fabricates numbers.\n\n"
            "To populate this section, run evaluation in the notebook on the "
            "test set and save the results, e.g.:\n\n"
            "```python\n"
            "import json\n"
            "metrics = {\n"
            '    \"accuracy\": ...,\n'
            '    \"precision\": ...,\n'
            '    \"recall\": ...,\n'
            '    \"f1_score\": ...,\n'
            '    \"confusion_matrix\": [[tn, fp], [fn, tp]],\n'
            "}\n"
            "with open('models/metrics.json', 'w') as f:\n"
            "    json.dump(metrics, f)\n"
            "```\n"
            "Then reload the app."
        )
    else:
        with open(metrics_path, "r") as f:
            metrics = json.load(f)

        cols = st.columns(4)
        for col, key in zip(cols, ["accuracy", "precision", "recall", "f1_score"]):
            if key in metrics:
                value = metrics[key]
                display_value = (
                    f"{value * 100:.2f}%"
                    if isinstance(value, (int, float)) and value <= 1
                    else str(value)
                )
                col.metric(key.replace("_", " ").title(), display_value)

        if "confusion_matrix" in metrics:
            st.markdown("**Confusion matrix**")
            st.table(metrics["confusion_matrix"])

        extra_keys = set(metrics.keys()) - {
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "confusion_matrix",
        }
        if extra_keys:
            st.markdown("**Additional reported metrics**")
            st.json({k: metrics[k] for k in extra_keys})
    card_close()

# =========================================================================
# ABOUT
# =========================================================================
with tab_about:
    hero(
        "About this project",
        "What this app is, how it was built, and what it isn't.",
    )

    card_open("Objective")
    st.markdown(
        "Build a deep learning image classification system using a "
        "convolutional neural network (CNN) that analyzes chest X-ray images "
        "and classifies them as **NORMAL** or **PNEUMONIA** — demonstrating "
        "how computer vision can extract visual patterns from medical images."
    )
    card_close()

    card_open("Technologies used")
    pill_row(["Python", "PyTorch", "torchvision", "Streamlit", "PIL / Pillow", "NumPy"])
    card_close()

    card_open("Approach")
    st.markdown(
        "A custom CNN (not a pretrained backbone) was trained from scratch on "
        "grayscale chest X-ray images resized to 96×96. Images were split "
        "70% / 15% / 15% into train, validation, and test sets, loaded via "
        "`torchvision.datasets.ImageFolder`, and trained with Adam and "
        "cross-entropy loss. See the **Model Insights** tab for the full "
        "configuration."
    )
    card_close()

    card_open("Dataset")
    st.markdown(
        "Chest X-ray images (NORMAL / PNEUMONIA), sourced from a public "
        "Kaggle dataset. The raw dataset is not bundled with this repository "
        "due to its size — see `data/data.txt` for the source link."
    )
    card_close()

    card_open("Limitations")
    st.markdown(
        """
- Trained on a specific public dataset; may not generalize to X-rays from
  different equipment, populations, or imaging protocols.
- Binary classification only — it does not localize findings or detect
  other thoracic conditions.
- Performance depends on image quality; blurry, cropped, or non-chest-X-ray
  images can produce unreliable results.
- This is a personal / educational project, not a validated clinical tool.
"""
    )
    card_close()

    st.write("")
    disclaimer_banner(DISCLAIMER)
