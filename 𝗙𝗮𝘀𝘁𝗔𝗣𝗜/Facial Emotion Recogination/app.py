"""
Facial Emotion Recognition - Streamlit App (Neumorphism, Light Theme)

Run with:  streamlit run app.py

Pages:
    1. Home     -> short intro
    2. Predict  -> upload a face photo, get the emotion
    3. About    -> full explanation of the project

How to run (2 terminals):
    1) uvicorn fastapi_app:app --port 8000     <- the model server
    2) streamlit run app.py                    <- this app
"""

import io
import os

import requests
import streamlit as st
from PIL import Image


# =====================================================================
# 1. BASIC SETTINGS
# =====================================================================

# Folder where this file lives (so paths work from anywhere)
APP_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Address of the FastAPI server (change it here, or set the API_URL variable)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

LOGO_PATH = os.path.join(APP_FOLDER, "logo.png")
SAMPLE_PATH = os.path.join(APP_FOLDER, "sample.jpg")

# Emoji + short text for every emotion
EMOTION_INFO = {
    "angry":    {"emoji": "😠", "text": "Frowning brows and tight lips."},
    "disgust":  {"emoji": "🤢", "text": "Wrinkled nose and raised upper lip."},
    "fear":     {"emoji": "😨", "text": "Wide eyes and a tense mouth."},
    "happy":    {"emoji": "😄", "text": "Smiling mouth and raised cheeks."},
    "neutral":  {"emoji": "😐", "text": "A relaxed face with no strong expression."},
    "sad":      {"emoji": "😢", "text": "Drooping eyes and a downturned mouth."},
    "surprise": {"emoji": "😲", "text": "Raised brows and an open mouth."},
}

# Page setup (must be the first Streamlit command)
st.set_page_config(
    page_title="Facial Emotion Recognition",
    page_icon="🙂",
    layout="wide",
)


# =====================================================================
# 2. NEUMORPHISM STYLE (CSS)
# =====================================================================
# Neumorphism = soft shapes made with TWO shadows:
#   a dark shadow (bottom-right) and a white shadow (top-left).
#   "Raised" look  -> normal shadow
#   "Pressed" look -> inset shadow

CSS = """
<style>
:root {
    --bg: #e0e5ec;
    --dark: #a3b1c6;
    --light: #ffffff;
    --text: #3d4468;
    --muted: #7b84a3;
    --accent: #5b7cfa;
    --accent2: #8f6bff;
    --raised: 9px 9px 18px var(--dark), -9px -9px 18px var(--light);
    --raised-small: 5px 5px 10px var(--dark), -5px -5px 10px var(--light);
    --pressed: inset 6px 6px 12px var(--dark), inset -6px -6px 12px var(--light);
}

/* ---------- page background ---------- */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg);
    color: var(--text);
}
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2.2rem; max-width: 1150px; }
h1, h2, h3, h4, p, li, label, span { color: var(--text); }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
    background: var(--bg);
    box-shadow: 6px 0 14px rgba(163, 177, 198, 0.45);
}
[data-testid="stSidebar"] [role="radiogroup"] { gap: 14px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: var(--bg);
    border-radius: 16px;
    padding: 12px 18px;
    box-shadow: var(--raised-small);
    cursor: pointer;
    transition: all 0.2s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    box-shadow: var(--pressed);
    color: var(--accent);
    font-weight: 700;
}
/* hide the small round radio dot */
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none; }
[data-testid="stSidebar"] [data-baseweb="radio"] > div:first-child { display: none; }

/* ---------- reusable cards ---------- */
.card {
    background: var(--bg);
    border-radius: 24px;
    padding: 26px 28px;
    margin-bottom: 26px;
    box-shadow: var(--raised);
}
.card h3 { margin: 0 0 10px 0; font-size: 1.25rem; }
.card p, .card li { color: var(--text); line-height: 1.7; font-size: 0.98rem; }
.card ul { padding-left: 20px; margin: 6px 0 0 0; }

.pressed {
    background: var(--bg);
    border-radius: 18px;
    padding: 16px 18px;
    box-shadow: var(--pressed);
}

/* ---------- hero (top banner) ---------- */
.hero { text-align: center; padding: 34px 20px; }
.hero h1 { font-size: 2.5rem; margin: 6px 0 8px 0; font-weight: 800; }
.hero p { color: var(--muted); font-size: 1.1rem; max-width: 720px; margin: 0 auto; }
.badge {
    display: inline-block;
    padding: 6px 16px;
    margin: 6px 4px;
    border-radius: 30px;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--accent);
    box-shadow: var(--raised-small);
}

/* ---------- stat tiles ---------- */
.stat-row { display: flex; gap: 18px; flex-wrap: wrap; margin-bottom: 26px; }
.stat {
    flex: 1;
    min-width: 170px;
    text-align: center;
    padding: 22px 12px;
    border-radius: 22px;
    box-shadow: var(--raised);
}
.stat .num { font-size: 2rem; font-weight: 800; color: var(--accent); }
.stat .label { font-size: 0.85rem; color: var(--muted); margin-top: 2px; }

/* ---------- progress bars ---------- */
.bar-row { display: flex; align-items: center; gap: 14px; margin: 12px 0; }
.bar-name { width: 90px; font-size: 0.9rem; font-weight: 600; }
.bar-track {
    flex: 1;
    height: 16px;
    border-radius: 10px;
    box-shadow: var(--pressed);
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.bar-value { width: 70px; text-align: right; font-size: 0.88rem; color: var(--muted); }

/* ---------- pipeline steps ---------- */
.step { display: flex; gap: 16px; align-items: flex-start; margin: 14px 0; }
.step-num {
    min-width: 40px; height: 40px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; color: var(--accent);
    box-shadow: var(--raised-small);
}
.step-body b { display: block; margin-bottom: 2px; }
.step-body span { color: var(--muted); font-size: 0.93rem; }

/* ---------- table ---------- */
.nm-table { width: 100%; border-collapse: separate; border-spacing: 0 10px; }
.nm-table th { text-align: left; color: var(--muted); font-size: 0.82rem; padding: 4px 14px; }
.nm-table td { padding: 12px 14px; font-size: 0.95rem; }
.nm-table tr.row td { background: var(--bg); box-shadow: inset 3px 3px 6px var(--dark), inset -3px -3px 6px var(--light); }
.nm-table tr.row td:first-child { border-radius: 14px 0 0 14px; }
.nm-table tr.row td:last-child { border-radius: 0 14px 14px 0; }
.nm-table tr.best td { color: var(--accent); font-weight: 700; }

/* ---------- result box on Predict page ---------- */
.result { text-align: center; padding: 30px 20px; }
.result .big-emoji { font-size: 4.5rem; }
.result .emotion { font-size: 2rem; font-weight: 800; text-transform: capitalize; }
.result .conf { color: var(--accent); font-size: 1.1rem; font-weight: 600; }

/* ---------- Streamlit widgets ---------- */
.stButton > button {
    background: var(--bg);
    color: var(--accent);
    border: none;
    border-radius: 16px;
    padding: 12px 30px;
    font-weight: 700;
    box-shadow: var(--raised-small);
    transition: all 0.2s ease;
}
.stButton > button:hover { color: var(--accent2); box-shadow: var(--raised); }
.stButton > button:active { box-shadow: var(--pressed); }

[data-testid="stFileUploaderDropzone"] {
    background: var(--bg);
    border: none;
    border-radius: 20px;
    box-shadow: var(--pressed);
    padding: 26px;
}
[data-testid="stFileUploaderDropzone"] button {
    background: var(--bg); color: var(--accent); border: none;
    border-radius: 12px; box-shadow: var(--raised-small);
}
[data-testid="stCameraInput"] > div { border-radius: 20px; box-shadow: var(--pressed); background: var(--bg); }
[data-testid="stImage"] img { border-radius: 22px; box-shadow: var(--raised); }
[data-testid="stAlert"] { border-radius: 18px; box-shadow: var(--raised-small); border: none; }
[data-testid="stToggle"] label, [data-testid="stCheckbox"] label { color: var(--text); }

.footer { text-align: center; color: var(--muted); font-size: 0.85rem; margin: 30px 0 10px 0; }
</style>
"""


# =====================================================================
# 3. SMALL HELPER FUNCTIONS (they just build HTML)
# =====================================================================

def clean(html):
    """Remove leading spaces so Streamlit does not treat HTML as code."""
    lines = [line.strip() for line in html.strip().splitlines()]
    return "\n".join(line for line in lines if line)


def show_html(html):
    """Show an HTML string on the page."""
    st.markdown(clean(html), unsafe_allow_html=True)


def card(title, body):
    """A raised card with a title and some HTML inside."""
    show_html(f'<div class="card"><h3>{title}</h3>{body}</div>')


def stat_tiles(items):
    """A row of big numbers. items = [(number, label), ...]"""
    tiles = ""
    for number, label in items:
        tiles += f'<div class="stat"><div class="num">{number}</div><div class="label">{label}</div></div>'
    show_html(f'<div class="stat-row">{tiles}</div>')


def bars_html(items, max_value, unit="", decimals=1):
    """Horizontal bars. items = [(name, value), ...]"""
    rows = ""
    for name, value in items:
        width = max(2, value / max_value * 100)
        rows += (
            f'<div class="bar-row">'
            f'<div class="bar-name">{name}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{width:.1f}%"></div></div>'
            f'<div class="bar-value">{value:,.{decimals}f}{unit}</div>'
            f'</div>'
        )
    return rows


def steps_html(steps):
    """Numbered steps. steps = [(title, description), ...]"""
    out = ""
    for number, (title, text) in enumerate(steps, start=1):
        out += (
            f'<div class="step"><div class="step-num">{number}</div>'
            f'<div class="step-body"><b>{title}</b><span>{text}</span></div></div>'
        )
    return out


def table_html(headers, rows, best_row=None):
    """Simple table. best_row = index of the row to highlight."""
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = ""
    for index, row in enumerate(rows):
        css = "row best" if index == best_row else "row"
        cells = "".join(f"<td>{cell}</td>" for cell in row)
        body += f'<tr class="{css}">{cells}</tr>'
    return f'<table class="nm-table"><tr>{head}</tr>{body}</table>'


# =====================================================================
# 4. FASTAPI CONNECTION
# =====================================================================
# The model lives inside the FastAPI server (fastapi_app.py).
# This Streamlit app only SENDS the image and SHOWS the answer.
#
#   Streamlit (this file)  --POST /predict-->  FastAPI  -->  ResNet18
#   Streamlit (this file)  <--- JSON result --  FastAPI  <--  ResNet18

def check_api():
    """Ask the API '/health'. Returns (True, info) or (False, error text)."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        if response.status_code == 200:
            return True, response.json()
        return False, f"API answered with status {response.status_code}"
    except requests.exceptions.RequestException:
        return False, "API is not running"


def prepare_image(image):
    """
    Training images were GRAYSCALE, so we make the photo grayscale too
    (but keep 3 channels because ResNet18 expects RGB). Returns PNG bytes.
    """
    gray = image.convert("L").convert("RGB")
    buffer = io.BytesIO()
    gray.save(buffer, format="PNG")
    return buffer.getvalue()


def predict_with_api(image):
    """
    Send the image to FastAPI /predict.
    Returns (result_dict, None) when OK, or (None, error_message) when not.
    """
    try:
        response = requests.post(
            f"{API_URL}/predict",
            files={"file": ("face.png", prepare_image(image), "image/png")},
            timeout=60,
        )
    except requests.exceptions.RequestException:
        return None, f"Could not reach the API at {API_URL}. Is it running?"

    if response.status_code != 200:
        return None, f"API error {response.status_code}: {response.text}"

    return response.json(), None



# =====================================================================
# 5. PAGE: HOME
# =====================================================================

def page_home():
    show_html("""
    <div class="card hero">
        <div class="badge">Deep Learning</div>
        <div class="badge">Transfer Learning</div>
        <div class="badge">ResNet18</div>
        <div class="badge">FastAPI</div>
        <div class="badge">FER2013</div>
        <h1>Facial Emotion Recognition</h1>
        <p>Upload a face photo and our trained ResNet18 model will tell you
        which of 7 emotions the face is showing - in just a moment.</p>
    </div>
    """)

    stat_tiles([
        ("67.07%", "Test accuracy"),
        ("7", "Emotions detected"),
        ("35,887", "Images in dataset"),
        ("128 x 128", "Model input size"),
    ])

    # Show all 7 emotions
    tiles = ""
    for name, info in EMOTION_INFO.items():
        tiles += (
            f'<div class="stat" style="min-width:90px;padding:18px 6px">'
            f'<div style="font-size:2.2rem">{info["emoji"]}</div>'
            f'<div class="label" style="text-transform:capitalize;font-weight:600">{name}</div></div>'
        )
    card("The 7 emotions it knows", f'<div class="stat-row" style="margin:0">{tiles}</div>')

    show_html("""
    <div class="card">
        <h3>How to use</h3>
        <ul>
            <li>Open the <b>Predict</b> page from the left menu.</li>
            <li>Upload a clear, front-facing photo (or use your camera).</li>
            <li>Click <b>Predict Emotion</b> and see the result with confidence scores.</li>
            <li>Want the full story? Open the <b>About</b> page.</li>
        </ul>
    </div>
    """)


# =====================================================================
# 6. PAGE: PREDICT
# =====================================================================

def page_predict():
    st.markdown("## Predict Emotion")
    st.caption("Upload a clear, front-facing face photo for the best result.")

    # --- Check that the FastAPI server is running ---
    api_ok, api_info = check_api()
    if not api_ok:
        card("FastAPI server is offline", f"""
            <p>{api_info}. Start it in another terminal:</p>
            <div class="pressed"><code>uvicorn fastapi_app:app --port 8000</code></div>
            <p>Then refresh this page. Looking for it at: <b>{API_URL}</b></p>
        """)
        return

    left, right = st.columns(2, gap="large")

    # ---------- LEFT: choose an image ----------
    with left:
        use_camera = st.toggle("Use camera instead of upload")

        if use_camera:
            picture = st.camera_input("Take a photo")
        else:
            picture = st.file_uploader("Upload a face image", type=["jpg", "jpeg", "png"])

        use_sample = st.checkbox("Or try the sample image")
        if use_sample and os.path.exists(SAMPLE_PATH):
            picture = SAMPLE_PATH   # a file path also works with Image.open

        image = None
        if picture is not None:
            image = Image.open(picture).convert("RGB")
            st.image(image, caption="Your image", width=320)

        predict_clicked = st.button("Predict Emotion", disabled=(image is None))

    # ---------- RIGHT: show the result ----------
    with right:
        if image is None:
            card("Result", "<p>Your prediction will appear here after you add an image.</p>")
        elif predict_clicked:
            with st.spinner("Sending image to the API..."):
                result, error = predict_with_api(image)

            if error:
                st.error(error)
                return

            scores = result["emotion_scores"]        # {"happy": 80.5, ...}
            best = result["predicted_emotion"]       # emotion with highest score
            info = EMOTION_INFO.get(best, {"emoji": "🙂", "text": ""})

            show_html(f"""
            <div class="card result">
                <div class="big-emoji">{info['emoji']}</div>
                <div class="emotion">{best}</div>
                <div class="conf">{result["confidence"]:.1f}% confident</div>
                <p style="color:#7b84a3">{info['text']}</p>
            </div>
            """)

            # All 7 scores, highest first
            ordered = sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
            card("All emotion scores", bars_html(ordered, max_value=100, unit="%"))

            if result["confidence"] < 50:
                st.info("The model is not very sure about this one. Try a clearer, front-facing photo.")
        else:
            card("Result", "<p>Image is ready. Click <b>Predict Emotion</b>.</p>")


# =====================================================================
# 7. PAGE: ABOUT (full project explanation)
# =====================================================================

def page_about():
    st.markdown("## About This Project")

    # ---- Overview ----
    card("1. Project overview", """
        <p><b>Facial Emotion Recognition</b> is a deep learning project that looks at a face image
        and predicts the emotion shown on it. It can tell 7 emotions:
        <b>angry, disgust, fear, happy, neutral, sad and surprise</b>.</p>
        <p>The project has two parts: first we <b>trained</b> models in Google Colab (on a Tesla T4 GPU),
        then we built this web app so anyone can <b>use</b> the best model without writing code.</p>
    """)

    stat_tiles([
        ("67.07%", "ResNet18 test accuracy"),
        ("55.39%", "Scratch CNN accuracy"),
        ("+11.7 pts", "Gain from transfer learning"),
        ("7,178", "Unseen test images"),
    ])

    # ---- Problem ----
    card("2. Problem and why it matters", """
        <p>Computers do not understand feelings by themselves. If a machine can read facial expressions,
        it can be used in customer feedback tools, online learning (is the student confused?),
        driver safety, games and mental-wellness apps.</p>
        <p>The task is hard because many expressions look alike (for example <i>fear</i> and <i>surprise</i>),
        the photos are tiny, and even humans do not always agree on the label.</p>
    """)

    # ---- Dataset ----
    train_counts = [("happy", 7215), ("neutral", 4965), ("sad", 4830), ("fear", 4097),
                    ("angry", 3995), ("surprise", 3171), ("disgust", 436)]
    card("3. Dataset - FER2013", f"""
        <p>We used the public <b>FER2013</b> dataset from Kaggle (msambare/fer2013).
        Every image is a <b>48 x 48 grayscale</b> face.</p>
        <ul>
            <li><b>Train folder:</b> 28,709 images (we kept 22,967 for training and 5,742 for validation = 80/20 split)</li>
            <li><b>Test folder:</b> 7,178 images (used only once, at the very end)</li>
            <li>Corrupted images were checked for before training.</li>
        </ul>
        <p style="margin-top:14px"><b>Images per emotion (train folder)</b></p>
        {bars_html(train_counts, max_value=7215, decimals=0)}
        <p><b>Problem:</b> the data is <i>imbalanced</i>. "Happy" has 7,215 images but "disgust" only 436.
        We fixed this with <b>class weights</b> (disgust gets about 3x importance in the loss).</p>
    """)

    # ---- Pipeline ----
    pipeline = [
        ("Collect data", "Download FER2013 from Kaggle with kagglehub."),
        ("Clean data", "Scan every image and remove corrupted files."),
        ("Split data", "Train (80%) / Validation (20%) / Test (given by the dataset)."),
        ("Transform images", "Convert to 3 channels, resize to 128x128, normalize like ImageNet."),
        ("Augment", "Random flip, small rotation, shift, zoom, brightness and random erasing - only on training images."),
        ("Train models", "Scratch CNN first, then transfer learning with ResNet18 and MobileNetV2."),
        ("Evaluate", "Accuracy, precision, recall, F1-score and confusion matrix on the test set."),
        ("Save and deploy", "Save the best model as a .pth file and use it in this Streamlit app."),
    ]
    card("4. Project pipeline", steps_html(pipeline))

    # ---- Model 1 ----
    arch_rows = [
        ("Conv block 1", "Conv 1 to 32, BatchNorm, ReLU, MaxPool", "48 to 24"),
        ("Conv block 2", "Conv 32 to 64, BatchNorm, ReLU, MaxPool", "24 to 12"),
        ("Conv block 3", "Conv 64 to 128, BatchNorm, ReLU, MaxPool", "12 to 6"),
        ("Conv block 4", "Conv 128 to 256, BatchNorm, ReLU, MaxPool", "6 to 3"),
        ("Dense layers", "Flatten 2304 to 512, Dropout 0.4, 512 to 7", "7 scores"),
    ]
    card("5. Model 1 - CNN built from scratch", f"""
        <p>Our first model was a small CNN made by hand (1.57 million parameters) using
        grayscale 48x48 input, Adam optimizer (lr 0.001), CrossEntropy loss, a learning-rate
        scheduler and early stopping.</p>
        {table_html(["Layer", "What it does", "Image size"], arch_rows)}
        <p><b>Result: 55.39% test accuracy.</b> Training accuracy reached about 84% while validation stayed near 59% -
        a clear sign of <b>overfitting</b> (the model memorised training images). Training stopped early at epoch 12.</p>
    """)

    # ---- Model 2 ----
    card("6. Model 2 - Transfer learning (the final model)", """
        <p><b>Transfer learning</b> means we start from a model already trained on millions of
        ImageNet photos. It already knows edges, shapes and textures - we only teach it our 7 emotions.</p>
        <ul>
            <li><b>Last layer replaced:</b> Dropout(0.4) then Linear(512 to 7).</li>
            <li><b>Phase 1 (5 epochs):</b> freeze the body, train only the new last layer (lr 0.001).</li>
            <li><b>Phase 2 (up to 15 epochs):</b> unfreeze everything and fine-tune gently (lr 0.0001) with early stopping (patience 5).</li>
            <li><b>Loss:</b> CrossEntropy with class weights and label smoothing 0.1 (helps with noisy labels).</li>
            <li><b>Extras:</b> mixed-precision training on GPU, batch size 64, image size 128x128.</li>
            <li>Two models were trained and compared: <b>ResNet18</b> and <b>MobileNetV2</b>.</li>
        </ul>
    """)

    # ---- Results ----
    results_rows = [
        ("ResNet18 (transfer learning)", "128 x 128", "~11.2 M", "67.07%"),
        ("MobileNetV2 (transfer learning)", "128 x 128", "~2.2 M", "63.62%"),
        ("CNN from scratch", "48 x 48", "1.57 M", "55.39%"),
    ]
    card("7. Results - model comparison", f"""
        {table_html(["Model", "Input size", "Parameters", "Test accuracy"], results_rows, best_row=0)}
        <p><b>ResNet18 won</b> and is the model used in this app. Transfer learning improved accuracy
        by about <b>11.7 percentage points</b> over the scratch CNN.</p>
    """)

    f1_scores = [("happy", 86.9), ("surprise", 77.7), ("neutral", 64.1), ("disgust", 63.3),
                 ("angry", 59.4), ("sad", 53.0), ("fear", 49.3)]
    card("8. ResNet18 - F1-score for each emotion", f"""
        {bars_html(f1_scores, max_value=100, unit="%")}
        <p><b>What we learn:</b> "Happy" and "surprise" are easy (clear shapes like a smile or open mouth).
        "Fear" and "sad" are hardest because they look like other emotions. Overall macro F1 = 64.8%.</p>
    """)

    # ---- How prediction works ----
    predict_steps = [
        ("You upload a photo", "Any JPG or PNG image."),
        ("Streamlit sends it", "The image goes to the FastAPI server with a POST request to /predict."),
        ("FastAPI pre-processing", "Resize to 128x128 and normalize like ImageNet."),
        ("ResNet18 forward pass", "The model produces 7 raw scores, softmax turns them into percentages."),
        ("JSON answer", "The API sends back the emotion, the confidence and all 7 scores. Streamlit shows them."),
    ]
    card("9. How a prediction works in this app", steps_html(predict_steps))

    # ---- Architecture of the app ----
    card("10. App structure - FastAPI + Streamlit", """
        <p>The project has <b>two programs</b> that talk to each other:</p>
        <ul>
            <li><b>fastapi_app.py</b> (backend): loads the ResNet18 model once and gives an
            endpoint <code>POST /predict</code> to predict, <code>GET /health</code> to check status and <code>GET /</code> for model info.</li>
            <li><b>app.py</b> (frontend): this screen. It sends the image to the API and shows the result.</li>
        </ul>
        <p>Why split them? The model can be reused by any other app (mobile, website),
        and the screen can change without touching the model code.</p>
        <p><b>Run in two terminals:</b></p>
        <div class="pressed"><code>uvicorn fastapi_app:app --port 8000</code></div>
        <p></p>
        <div class="pressed"><code>streamlit run app.py</code></div>
    """)

    # ---- Limitations ----
    card("11. Limitations and future work", """
        <ul>
            <li>FER2013 labels are noisy and photos are low quality, so accuracy has a natural ceiling (even humans only reach about 65% on it).</li>
            <li>The model reads <b>facial expression</b>, not real inner feelings.</li>
            <li>Works best on one clear, front-facing face. Side views, sunglasses and dark photos reduce accuracy.</li>
            <li><b>Future ideas:</b> automatic face detection and cropping, real-time webcam video, bigger models
            (EfficientNet), test-time augmentation and training on more diverse datasets like AffectNet.</li>
        </ul>
    """)

    # ---- Tech stack ----
    badges = "".join(f'<span class="badge">{t}</span>' for t in
                     ["Python", "PyTorch", "Torchvision", "ResNet18", "Scikit-learn", "Pandas",
                      "Matplotlib", "Seaborn", "Pillow", "Streamlit", "FastAPI", "Google Colab"])
    card("12. Tech stack", f"<div>{badges}</div>")


# =====================================================================
# 8. MAIN - sidebar menu and page switching
# =====================================================================

def main():
    show_html(CSS)

    # ---- Sidebar ----
    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=120)
        st.markdown("### Emotion Recognition")
        page = st.radio("Menu", ["🏠  Home", "🎯  Predict", "📖  About"], label_visibility="collapsed")
        st.caption("ResNet18 · FER2013 · PyTorch")

        # Small live status of the API
        api_ok, _ = check_api()
        st.markdown("🟢 API online" if api_ok else "🔴 API offline")

    # ---- Show the chosen page ----
    if "Home" in page:
        page_home()
    elif "Predict" in page:
        page_predict()
    else:
        page_about()

    show_html('<div class="footer">Facial Emotion Recognition · Built with PyTorch and Streamlit</div>')


main()