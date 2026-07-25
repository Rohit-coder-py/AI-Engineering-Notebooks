"""
app.py - Streamlit deployment for the Cats vs Dogs CNN

Upload an image, get a Cat / Dog prediction with confidence.
Run with:  streamlit run app.py
"""

import os

import streamlit as st
from PIL import Image

from src.infer import load_model, predict_image

MODEL_PATH = "models/cat_dog_cnn.pth"

st.set_page_config(
    page_title="Cats vs Dogs Classifier",
    page_icon="\U0001F43E",
    layout="wide",
)

# ==========================
# Styling - dark, jewel-tone, Cormorant Garamond + JetBrains Mono
# ==========================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
:root {
    --obsidian: #0b0d10;
    --panel: #14171c;
    --panel-border: #262b33;
    --emerald: #1f8a5f;
    --emerald-soft: #2fb37b;
    --oxblood: #6e1f2a;
    --oxblood-soft: #9b3346;
    --brass: #c9a24b;
    --text-main: #ece7dd;
    --text-dim: #8b9098;
}

.stApp {
    background: radial-gradient(circle at 20% -10%, #14181d 0%, var(--obsidian) 55%);
    color: var(--text-main);
    font-family: 'Cormorant Garamond', serif;
}

[data-testid="stSidebar"] {
    background: var(--panel);
    border-right: 1px solid var(--panel-border);
}

h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 600;
    color: var(--text-main);
    letter-spacing: 0.02em;
}

.eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--brass);
    margin-bottom: 0.3rem;
}

.hero-title {
    font-size: 3rem;
    line-height: 1.05;
    margin: 0 0 0.4rem 0;
}

.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.95rem;
    color: var(--text-dim);
    max-width: 640px;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, var(--brass), transparent);
    margin: 1.6rem 0;
    opacity: 0.5;
}

.result-card {
    background: var(--panel);
    border: 1px solid var(--panel-border);
    border-radius: 4px;
    padding: 1.6rem 1.8rem;
}

.result-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-dim);
}

.result-verdict {
    font-size: 2.4rem;
    font-weight: 600;
    margin: 0.2rem 0 0.8rem 0;
}

.verdict-cat { color: var(--emerald-soft); }
.verdict-dog { color: var(--oxblood-soft); }

.gauge-track {
    width: 100%;
    height: 10px;
    border-radius: 6px;
    background: var(--panel-border);
    overflow: hidden;
    display: flex;
}

.gauge-cat { background: var(--emerald); }
.gauge-dog { background: var(--oxblood); }

.gauge-caption {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-dim);
    display: flex;
    justify-content: space-between;
    margin-top: 0.5rem;
}

.info-block {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--text-dim);
    line-height: 1.7;
}

[data-testid="stFileUploader"] {
    border: 1px dashed var(--panel-border);
    border-radius: 4px;
    padding: 0.6rem;
    background: var(--panel);
}
</style>
""", unsafe_allow_html=True)

# ==========================
# Sidebar - model info
# ==========================
with st.sidebar:
    st.markdown('<div class="eyebrow">Architecture</div>', unsafe_allow_html=True)
    st.markdown("### CatDogCNN")
    st.markdown("""
<div class="info-block">
4x Conv2d + ReLU + MaxPool blocks (32 &rarr; 64 &rarr; 128 &rarr; 256 channels)<br>
&darr;<br>
Flatten<br>
&darr;<br>
FC 512 &rarr; FC 128 &rarr; FC 2<br><br>
Input: 224x224 RGB, ImageNet-normalized<br>
Loss: CrossEntropyLoss<br>
Optimizer: Adam (lr=0.001)
</div>
""", unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Pipeline</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="info-block">
Clean &rarr; Split (70/15/15) &rarr; Transform &rarr;<br>
Train + Validate &rarr; Evaluate &rarr; Save &rarr; Infer
</div>
""", unsafe_allow_html=True)

# ==========================
# Hero
# ==========================
st.markdown('<div class="eyebrow">Image Classification &middot; PyTorch CNN</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Cats vs Dogs</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Upload a photo and the model will decide - Cat or Dog - with a confidence score.</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ==========================
# Model loading
# ==========================
@st.cache_resource
def get_model():
    return load_model(MODEL_PATH)


if not os.path.exists(MODEL_PATH):
    st.markdown(f"""
<div class="result-card">
<div class="result-label">Model Not Found</div>
<div class="info-block" style="margin-top: 0.6rem;">
No trained weights at <code>{MODEL_PATH}</code> yet.<br><br>
Train the model first:<br>
1. Run the notebook (<code>Cats_vs_Dogs.ipynb</code>) end to end, or<br>
2. Run <code>python train.py --data "path/to/PetImages"</code> from the terminal<br><br>
Either one writes <code>models/cat_dog_cnn.pth</code>, and this app will pick it up automatically.
</div>
</div>
""", unsafe_allow_html=True)
    st.stop()

model = get_model()

# ==========================
# Upload + Predict
# ==========================
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="eyebrow">Upload</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drop an image (jpg / jpeg / png)",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)

with col_right:
    st.markdown('<div class="eyebrow">Result</div>', unsafe_allow_html=True)

    if uploaded_file is None:
        st.markdown("""
<div class="result-card">
<div class="info-block">Waiting for an image on the left.</div>
</div>
""", unsafe_allow_html=True)
    else:
        label, confidence, probs = predict_image(image, model)
        cat_prob, dog_prob = probs[0] * 100, probs[1] * 100

        verdict_class = "verdict-cat" if label == "Cat" else "verdict-dog"

        st.markdown(f"""
<div class="result-card">
    <div class="result-label">Prediction</div>
    <div class="result-verdict {verdict_class}">{label}</div>
    <div class="gauge-track">
        <div class="gauge-cat" style="width:{cat_prob}%;"></div>
        <div class="gauge-dog" style="width:{dog_prob}%;"></div>
    </div>
    <div class="gauge-caption">
        <span>Cat &middot; {cat_prob:.1f}%</span>
        <span>Dog &middot; {dog_prob:.1f}%</span>
    </div>
</div>
""", unsafe_allow_html=True)
