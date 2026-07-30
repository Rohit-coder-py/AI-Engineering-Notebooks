
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
# Styling - dark, jewel-tone but colorful, high-contrast
# ==========================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
:root {
    --obsidian: #0a0c10;
    --panel: #161a22;
    --panel-alt: #1c212b;
    --panel-border: #2d3444;

    --emerald: #22c98a;
    --emerald-glow: rgba(34, 201, 138, 0.35);
    --amber: #ffb84d;
    --oxblood: #ff5c72;
    --oxblood-glow: rgba(255, 92, 114, 0.35);
    --sapphire: #4ea6ff;
    --violet: #b18aff;

    --text-main: #f4f2ec;
    --text-dim: #aab1c0;
    --text-faint: #7b8296;
}

.stApp {
    background:
        radial-gradient(circle at 12% -10%, rgba(78, 166, 255, 0.10) 0%, transparent 40%),
        radial-gradient(circle at 90% 0%, rgba(177, 138, 255, 0.10) 0%, transparent 45%),
        radial-gradient(circle at 50% 100%, rgba(34, 201, 138, 0.06) 0%, transparent 50%),
        var(--obsidian);
    color: var(--text-main);
    font-family: 'Cormorant Garamond', serif;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--panel) 0%, var(--obsidian) 100%);
    border-right: 1px solid var(--panel-border);
}

h1, h2, h3 { font-family: 'Cormorant Garamond', serif; color: var(--text-main); }

/* -------- eyebrow / small labels -------- */
.eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--amber);
    font-weight: 600;
    margin-bottom: 0.4rem;
}

/* -------- hero -------- */
.hero-title {
    font-size: 3.4rem;
    font-weight: 700;
    line-height: 1.05;
    margin: 0 0 0.5rem 0;
    background: linear-gradient(90deg, #ffffff 0%, var(--sapphire) 55%, var(--violet) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem;
    color: var(--text-dim);
    max-width: 680px;
    line-height: 1.6;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, var(--sapphire), var(--violet), var(--oxblood), transparent);
    margin: 1.7rem 0;
    opacity: 0.6;
}

/* -------- sidebar blocks -------- */
.side-card {
    background: var(--panel-alt);
    border: 1px solid var(--panel-border);
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 1.1rem;
}

.info-block {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--text-dim);
    line-height: 1.75;
}

.info-block b, .info-block strong { color: var(--text-main); }

.chip-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; }

.chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.28rem 0.6rem;
    border-radius: 999px;
    border: 1px solid transparent;
    white-space: nowrap;
}
.chip-blue   { background: rgba(78, 166, 255, 0.14);  color: var(--sapphire); border-color: rgba(78, 166, 255, 0.35); }
.chip-violet { background: rgba(177, 138, 255, 0.14); color: var(--violet);  border-color: rgba(177, 138, 255, 0.35); }
.chip-green  { background: rgba(34, 201, 138, 0.14);  color: var(--emerald); border-color: rgba(34, 201, 138, 0.35); }
.chip-amber  { background: rgba(255, 184, 77, 0.14);  color: var(--amber);   border-color: rgba(255, 184, 77, 0.35); }
.chip-red    { background: rgba(255, 92, 114, 0.14);  color: var(--oxblood); border-color: rgba(255, 92, 114, 0.35); }

/* -------- upload / result cards -------- */
.section-card {
    background: var(--panel);
    border: 1px solid var(--panel-border);
    border-radius: 14px;
    padding: 1.7rem 1.9rem;
    height: 100%;
}

[data-testid="stFileUploaderDropzone"] {
    background: var(--panel-alt) !important;
    border: 1.5px dashed var(--sapphire) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploaderDropzone"] * {
    color: var(--text-main) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] svg { fill: var(--sapphire) !important; }
[data-testid="stBaseButton-secondary"] {
    background: linear-gradient(90deg, var(--sapphire), var(--violet)) !important;
    color: #0a0c10 !important;
    font-weight: 700 !important;
    border: none !important;
}
[data-testid="stFileUploaderDropzone"] small { color: var(--text-dim) !important; }

.result-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-faint);
    font-weight: 600;
}

.result-verdict {
    font-size: 3rem;
    font-weight: 700;
    margin: 0.3rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.verdict-cat { color: var(--emerald); text-shadow: 0 0 24px var(--emerald-glow); }
.verdict-dog { color: var(--oxblood); text-shadow: 0 0 24px var(--oxblood-glow); }

.gauge-track {
    width: 100%;
    height: 14px;
    border-radius: 8px;
    background: var(--panel-alt);
    overflow: hidden;
    display: flex;
    border: 1px solid var(--panel-border);
}

.gauge-cat { background: linear-gradient(90deg, #17a674, var(--emerald)); }
.gauge-dog { background: linear-gradient(90deg, var(--oxblood), #ff8a97); }

.gauge-caption {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--text-dim);
    display: flex;
    justify-content: space-between;
    margin-top: 0.6rem;
}
.gauge-caption span:first-child { color: var(--emerald); font-weight: 600; }
.gauge-caption span:last-child  { color: var(--oxblood); font-weight: 600; }

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2.4rem 1rem;
    color: var(--text-dim);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
}
.empty-state .glyph { font-size: 2.4rem; margin-bottom: 0.7rem; opacity: 0.85; }

.stat-row { display: flex; gap: 0.8rem; margin-top: 1.4rem; }
.stat-box {
    flex: 1;
    background: var(--panel-alt);
    border: 1px solid var(--panel-border);
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
}
.stat-box .stat-label { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-faint); }
.stat-box .stat-value { font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 700; margin-top: 0.15rem; }
</style>
""", unsafe_allow_html=True)

# ==========================
# Sidebar - model info
# ==========================
with st.sidebar:
    st.markdown('<div class="eyebrow">Architecture</div>', unsafe_allow_html=True)
    st.markdown("### CatDogCNN")
    st.markdown("""
<div class="side-card">
<div class="info-block">
<b>4x</b> Conv2d + ReLU + MaxPool blocks<br>
<span style="color:var(--sapphire)">32</span> &rarr;
<span style="color:var(--violet)">64</span> &rarr;
<span style="color:var(--amber)">128</span> &rarr;
<span style="color:var(--oxblood)">256</span> channels
&darr;<br>
Flatten &darr;<br>
FC <b>512</b> &rarr; FC <b>128</b> &rarr; FC <b>2</b>
</div>
<div class="chip-row">
    <span class="chip chip-blue">96x96 RGB</span>
    <span class="chip chip-violet">ImageNet norm</span>
</div>
<div class="chip-row">
    <span class="chip chip-amber">CrossEntropyLoss</span>
    <span class="chip chip-green">Adam &middot; lr 0.001</span>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="eyebrow">Pipeline</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="side-card">
<div class="chip-row">
    <span class="chip chip-blue">Clean</span>
    <span class="chip chip-violet">Split 70/15/15</span>
    <span class="chip chip-amber">Transform</span>
</div>
<div class="chip-row">
    <span class="chip chip-green">Train</span>
    <span class="chip chip-green">Validate</span>
    <span class="chip chip-red">Evaluate</span>
</div>
<div class="chip-row">
    <span class="chip chip-blue">Save</span>
    <span class="chip chip-violet">Infer</span>
</div>
</div>
""", unsafe_allow_html=True)

# ==========================
# Hero
# ==========================
st.markdown('<div class="eyebrow">Image Classification &middot; PyTorch CNN</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Cats vs Dogs \U0001F43E\U0001F415</div>', unsafe_allow_html=True)
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
<div class="section-card">
<div class="result-label" style="color: var(--oxblood);">Model Not Found</div>
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
<div class="section-card">
<div class="empty-state">
<div class="glyph">\U0001F31F</div>
Waiting for an image on the left.<br>Drop a cat or dog photo to see the verdict.
</div>
</div>
""", unsafe_allow_html=True)
    else:
        label, confidence, probs = predict_image(image, model)
        cat_prob, dog_prob = probs[0] * 100, probs[1] * 100

        verdict_class = "verdict-cat" if label == "Cat" else "verdict-dog"
        verdict_icon = "\U0001F431" if label == "Cat" else "\U0001F415"
        top_prob = max(cat_prob, dog_prob)
        runner_prob = min(cat_prob, dog_prob)

        st.markdown(f"""
<div class="section-card">
    <div class="result-label">Prediction</div>
    <div class="result-verdict {verdict_class}">{verdict_icon} {label}</div>
    <div class="gauge-track">
        <div class="gauge-cat" style="width:{cat_prob}%;"></div>
        <div class="gauge-dog" style="width:{dog_prob}%;"></div>
    </div>
    <div class="gauge-caption">
        <span>\U0001F431 Cat &middot; {cat_prob:.1f}%</span>
        <span>\U0001F415 Dog &middot; {dog_prob:.1f}%</span>
    </div>
    <div class="stat-row">
        <div class="stat-box">
            <div class="stat-label">Confidence</div>
            <div class="stat-value" style="color: var(--emerald);">{top_prob:.1f}%</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Runner-up</div>
            <div class="stat-value" style="color: var(--text-dim);">{runner_prob:.1f}%</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Margin</div>
            <div class="stat-value" style="color: var(--sapphire);">{(top_prob - runner_prob):.1f} pts</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)