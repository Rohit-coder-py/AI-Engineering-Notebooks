"""
Sentence Auto Completer Bot
----------------------------
A Streamlit app that predicts the next word / auto-completes sentences
using RNN and LSTM models trained (from scratch, in PyTorch) on a
dataset of famous quotes.

Run with:
    streamlit run app.py
"""

import pickle
import string
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import torch
import torch.nn as nn

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
GRAPHS_DIR = BASE_DIR / "graphs"

DATA_PATH = DATA_DIR / "qoute_dataset.csv"
VOCAB_PATH = MODELS_DIR / "vocab.pkl"
MAXLEN_PATH = MODELS_DIR / "max_len.pkl"
RNN_PATH = MODELS_DIR / "rnn_model.pth"
LSTM_PATH = MODELS_DIR / "lstm_model.pth"
TRAIN_CURVE_IMG = GRAPHS_DIR / "training vs validation loss.png"

VOCAB_SIZE = 10000
EMBEDDING_DIM = 50
RNN_UNITS = 128
DEVICE = torch.device("cpu")

# --------------------------------------------------------------------------
# Page config -- MUST be first Streamlit call
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Sentence Auto Completer Bot",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# CSS -- force a light, colourful, animated look regardless of the
# viewer's OS/browser dark-mode setting.
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* ---------- Force light backgrounds everywhere ---------- */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(135deg, #FBFAFF 0%, #F1EEFF 45%, #FFF3F8 100%) !important;
        color: #2D2A45 !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F5F3FF 0%, #ECE9FF 100%) !important;
        border-right: 1px solid #E5DEFF;
    }
    [data-testid="stSidebar"] * { color: #2D2A45 !important; }

    /* ---------- Animated gradient title ---------- */
    @keyframes gradientShift {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #7C6CF6, #F669C1, #6CD4F6, #7C6CF6);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 6s ease infinite;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        text-align: center;
        color: #6B6488 !important;
        font-size: 1.05rem;
        margin-bottom: 1.4rem;
        animation: fadeIn 1.4s ease;
    }

    /* ---------- Fade / rise-in animation ---------- */
    @keyframes fadeIn { from {opacity: 0;} to {opacity: 1;} }
    @keyframes riseIn {
        from {opacity: 0; transform: translateY(14px);}
        to   {opacity: 1; transform: translateY(0);}
    }
    .fade-card {
        animation: riseIn 0.55s ease-out;
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 6px 20px rgba(124, 108, 246, 0.12);
        border: 1px solid #EFEBFF;
        margin-bottom: 1rem;
    }

    /* ---------- Quote result card ---------- */
    @keyframes glow {
        0%,100% { box-shadow: 0 0 12px rgba(124,108,246,0.15); }
        50%     { box-shadow: 0 0 24px rgba(246,105,193,0.30); }
    }
    .quote-card {
        animation: riseIn 0.6s ease-out, glow 3.5s ease-in-out infinite;
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F5FF 100%);
        border-left: 6px solid #7C6CF6;
        border-radius: 14px;
        padding: 1.3rem 1.6rem;
        font-size: 1.25rem;
        font-style: italic;
        color: #362F5C !important;
        margin: 0.8rem 0 1.2rem 0;
    }

    /* ---------- Word chips ---------- */
    .chip {
        display: inline-block;
        padding: 0.35rem 0.9rem;
        margin: 0.25rem;
        border-radius: 999px;
        background: linear-gradient(90deg, #EDE9FF, #FFE9F6);
        color: #4B3F8F !important;
        font-weight: 600;
        font-size: 0.92rem;
        animation: riseIn 0.4s ease-out;
        border: 1px solid #E3DBFF;
    }

    /* ---------- Metric cards ---------- */
    .metric-box {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 0.9rem;
        text-align: center;
        box-shadow: 0 4px 14px rgba(124,108,246,0.10);
        border: 1px solid #EFEBFF;
        animation: riseIn 0.5s ease-out;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #7C6CF6 !important;
    }
    .metric-label {
        font-size: 0.82rem;
        color: #857EA6 !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    /* ---------- Buttons ---------- */
    .stButton>button {
        background: linear-gradient(90deg, #7C6CF6, #A98CF9) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.3rem !important;
        font-weight: 700 !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        box-shadow: 0 4px 12px rgba(124,108,246,0.30) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 18px rgba(124,108,246,0.40) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        background: #F5F3FF;
        border-radius: 10px 10px 0 0;
        color: #6B6488;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #7C6CF6 !important;
    }

    footer, [data-testid="stDecoration"] {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Model definitions (must match training notebook exactly)
# --------------------------------------------------------------------------
class RNNModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, rnn_units):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.rnn = nn.RNN(embedding_dim, rnn_units, batch_first=True)
        self.fc = nn.Linear(rnn_units, vocab_size)

    def forward(self, x):
        embedded = self.embedding(x)
        rnn_out, _ = self.rnn(embedded)
        return self.fc(rnn_out[:, -1, :])


class LSTMModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, rnn_units):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(embedding_dim, rnn_units, batch_first=True)
        self.fc = nn.Linear(rnn_units, vocab_size)

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        return self.fc(lstm_out[:, -1, :])


# --------------------------------------------------------------------------
# Cached resource loaders
# --------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_vocab_and_maxlen():
    with open(VOCAB_PATH, "rb") as f:
        vocab = pickle.load(f)
    with open(MAXLEN_PATH, "rb") as f:
        max_len = pickle.load(f)
    return vocab["word_to_index"], vocab["index_to_word"], max_len


@st.cache_resource(show_spinner=False)
def load_models():
    rnn = RNNModel(VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS)
    rnn.load_state_dict(torch.load(RNN_PATH, map_location=DEVICE))
    rnn.eval()

    lstm = LSTMModel(VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS)
    lstm.load_state_dict(torch.load(LSTM_PATH, map_location=DEVICE))
    lstm.eval()
    return {"RNN": rnn, "LSTM": lstm}


@st.cache_data(show_spinner=False)
def load_dataset():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["quote"]).reset_index(drop=True)
    return df


# --------------------------------------------------------------------------
# Text processing helpers (must mirror the training notebook exactly)
# --------------------------------------------------------------------------
_TRANSLATOR = str.maketrans("", "", string.punctuation)


def clean_text(text: str) -> str:
    return text.lower().translate(_TRANSLATOR)


def text_to_sequence(text: str, word_to_index: dict) -> list:
    return [word_to_index[w] for w in text.split() if w in word_to_index]


def pad_sequence_pre(seq: list, max_len: int) -> np.ndarray:
    padded = np.zeros((1, max_len), dtype=np.int64)
    length = min(len(seq), max_len)
    if length > 0:
        padded[0, -length:] = seq[-length:]
    return padded


def predict_topk(model, text, word_to_index, index_to_word, max_len, k=5):
    model.eval()
    seq = text_to_sequence(clean_text(text), word_to_index)
    padded = pad_sequence_pre(seq, max_len)
    tensor = torch.tensor(padded, dtype=torch.long)
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)[0]
    k = min(k, probs.shape[0])
    top_probs, top_idx = torch.topk(probs, k)
    words = [index_to_word.get(i.item(), "") for i in top_idx]
    confidences = [p.item() for p in top_probs]
    return list(zip(words, confidences))


def generate_sentence(model, seed_text, word_to_index, index_to_word, max_len, n_words):
    text = seed_text
    generated_words = []
    for _ in range(n_words):
        top = predict_topk(model, text, word_to_index, index_to_word, max_len, k=1)
        next_word = top[0][0] if top else ""
        if not next_word:
            break
        text += " " + next_word
        generated_words.append(next_word)
    return text, generated_words


# --------------------------------------------------------------------------
# Analytics helpers (all forward-pass / read-only -- no training here,
# the RNN and LSTM weights are the ones already trained in the notebook)
# --------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def compute_text_stats(df: pd.DataFrame):
    quotes_clean = df["quote"].str.lower().apply(lambda x: x.translate(_TRANSLATOR))
    word_counts = Counter()
    for q in quotes_clean:
        word_counts.update(q.split())
    lengths = quotes_clean.apply(lambda x: len(x.split()))
    top_authors = df["Author"].value_counts().head(10)
    return word_counts, lengths, top_authors


@st.cache_data(show_spinner=False)
def compute_model_eval(_models, word_to_index, index_to_word, max_len, df, sample_size=4000):
    """Forward-pass only evaluation (no training) of both models on a
    random sample of the next-word-prediction examples, so the metrics
    are real but stay fast enough for an interactive app."""
    quotes_clean = df["quote"].str.lower().apply(lambda x: x.translate(_TRANSLATOR))
    sequences = [text_to_sequence(q, word_to_index) for q in quotes_clean]

    X, y = [], []
    for seq in sequences:
        for i in range(1, len(seq)):
            X.append(seq[:i])
            y.append(seq[i])

    rng = np.random.default_rng(42)
    if len(X) > sample_size:
        idx = rng.choice(len(X), size=sample_size, replace=False)
        X = [X[i] for i in idx]
        y = [y[i] for i in idx]

    X_padded = np.zeros((len(X), max_len), dtype=np.int64)
    for i, seq in enumerate(X):
        length = min(len(seq), max_len)
        if length > 0:
            X_padded[i, -length:] = seq[-length:]

    X_tensor = torch.tensor(X_padded, dtype=torch.long)
    y_tensor = torch.tensor(y, dtype=torch.long)
    criterion = nn.CrossEntropyLoss()

    results = {}
    for name, model in _models.items():
        model.eval()
        with torch.no_grad():
            logits = model(X_tensor)
            loss = criterion(logits, y_tensor).item()
            preds = torch.argmax(logits, dim=1)
            acc = (preds == y_tensor).float().mean().item()
        n_params = sum(p.numel() for p in model.parameters())
        results[name] = {"loss": loss, "accuracy": acc, "params": n_params}
    return results


# --------------------------------------------------------------------------
# Load everything
# --------------------------------------------------------------------------
word_to_index, index_to_word, max_len = load_vocab_and_maxlen()
models = load_models()
df = load_dataset()

# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    model_choice = st.radio(
        "Model",
        ["LSTM (recommended)", "RNN", "Compare Both"],
        index=0,
    )
    top_k = st.slider("Suggestions to show (top-k)", 3, 10, 5)
    n_words = st.slider("Words to auto-generate", 1, 30, 10)
    typing_speed = st.slider("Typing animation speed", 0.02, 0.35, 0.12, step=0.01)

    st.markdown("---")
    st.markdown("### 📚 About the data")
    st.caption(
        f"Trained on **{len(df):,}** famous quotes from **{df['Author'].nunique():,}** authors. "
        f"Vocabulary size: **{len(word_to_index):,}** words. Max sequence length: **{max_len}**."
    )
    st.markdown("---")
    st.caption("Built with PyTorch + Streamlit · RNN & LSTM trained from scratch")

# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.markdown('<div class="hero-title">✨ Sentence Auto Completer Bot ✨</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Next-word prediction &amp; sentence auto-completion, '
    'powered by RNN and LSTM networks trained from scratch on 3,000+ famous quotes.</div>',
    unsafe_allow_html=True,
)

tab_predict, tab_analytics, tab_about = st.tabs(["🔮 Predict & Generate", "📊 Analytics", "ℹ️ About"])

# ==========================================================================
# TAB 1 -- Predict & Generate
# ==========================================================================
with tab_predict:
    st.markdown('<div class="fade-card">', unsafe_allow_html=True)
    seed_text = st.text_input(
        "Start typing a sentence…",
        value="the only way to do great work is",
        placeholder="e.g. life is what happens when",
    )
    col_a, col_b = st.columns(2)
    predict_clicked = col_a.button("🔍 Predict Next Word", width="stretch")
    generate_clicked = col_b.button("✨ Auto-Complete Sentence", width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

    def _selected_models():
        if model_choice == "Compare Both":
            return ["RNN", "LSTM"]
        return ["LSTM"] if "LSTM" in model_choice else ["RNN"]

    if predict_clicked and seed_text.strip():
        chosen = _selected_models()
        cols = st.columns(len(chosen))
        for col, name in zip(cols, chosen):
            with col:
                st.markdown(f"**{name} model**")
                with st.spinner(f"Thinking with {name}…"):
                    time.sleep(0.25)
                    preds = predict_topk(models[name], seed_text, word_to_index, index_to_word, max_len, k=top_k)
                if not preds:
                    st.info("No prediction available — try different words (they may be outside the vocabulary).")
                else:
                    fig = go.Figure(
                        go.Bar(
                            x=[p[1] * 100 for p in preds][::-1],
                            y=[p[0] for p in preds][::-1],
                            orientation="h",
                            marker=dict(
                                color=[p[1] * 100 for p in preds][::-1],
                                colorscale=[[0, "#D9CFFF"], [1, "#7C6CF6"]],
                            ),
                            text=[f"{p[1]*100:.1f}%" for p in preds][::-1],
                            textposition="outside",
                        )
                    )
                    fig.update_layout(
                        height=340,
                        margin=dict(l=10, r=10, t=10, b=10),
                        plot_bgcolor="#FFFFFF",
                        paper_bgcolor="#FFFFFF",
                        font=dict(color="#2D2A45"),
                        xaxis=dict(title="Confidence (%)", gridcolor="#F0EDFF"),
                    )
                    st.plotly_chart(fig, width="stretch")
                    chips = "".join(f'<span class="chip">{w}</span>' for w, _ in preds)
                    st.markdown(chips, unsafe_allow_html=True)

    if generate_clicked and seed_text.strip():
        chosen = _selected_models()
        cols = st.columns(len(chosen))
        for col, name in zip(cols, chosen):
            with col:
                st.markdown(f"**{name} model**")
                placeholder = st.empty()
                running_text = seed_text
                placeholder.markdown(f'<div class="quote-card">{running_text} ▌</div>', unsafe_allow_html=True)
                _, words = generate_sentence(models[name], seed_text, word_to_index, index_to_word, max_len, n_words)
                for w in words:
                    running_text += " " + w
                    placeholder.markdown(f'<div class="quote-card">{running_text} ▌</div>', unsafe_allow_html=True)
                    time.sleep(typing_speed)
                placeholder.markdown(f'<div class="quote-card">“{running_text}”</div>', unsafe_allow_html=True)
                st.caption(f"Generated {len(words)} word(s) with the {name} model.")

    if not seed_text.strip():
        st.info("👆 Type a sentence above, then click **Predict Next Word** or **Auto-Complete Sentence**.")

# ==========================================================================
# TAB 2 -- Analytics
# ==========================================================================
with tab_analytics:
    word_counts, lengths, top_authors = compute_text_stats(df)
    eval_results = compute_model_eval(models, word_to_index, index_to_word, max_len, df)

    st.markdown("#### 📌 Dataset & Model Overview")
    metric_cols = st.columns(5)
    metrics = [
        ("Quotes", f"{len(df):,}"),
        ("Authors", f"{df['Author'].nunique():,}"),
        ("Vocabulary", f"{len(word_to_index):,}"),
        ("Max Seq Len", f"{max_len}"),
        ("Training Pairs", f"{sum(max(len(clean_text(q).split()) - 1, 0) for q in df['quote']):,}"),
    ]
    for col, (label, value) in zip(metric_cols, metrics):
        col.markdown(
            f'<div class="metric-box"><div class="metric-value">{value}</div>'
            f'<div class="metric-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🏋️ Training History (RNN vs LSTM)")
    if TRAIN_CURVE_IMG.exists():
        st.image(str(TRAIN_CURVE_IMG), width="stretch")
    else:
        st.info("Training curve image not found in graphs/.")

    st.markdown("#### 🧪 Evaluation — Forward-pass Loss & Accuracy")
    st.caption("Computed on a sample of held-out next-word examples using the already-trained weights (no retraining).")
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(
            go.Bar(
                x=list(eval_results.keys()),
                y=[v["loss"] for v in eval_results.values()],
                marker_color=["#A98CF9", "#F6A6D8"],
                text=[f"{v['loss']:.3f}" for v in eval_results.values()],
                textposition="outside",
            )
        )
        fig.update_layout(
            title="Cross-Entropy Loss", height=320, plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
            font=dict(color="#2D2A45"), yaxis=dict(gridcolor="#F0EDFF"),
        )
        st.plotly_chart(fig, width="stretch")
    with c2:
        fig = go.Figure(
            go.Bar(
                x=list(eval_results.keys()),
                y=[v["accuracy"] * 100 for v in eval_results.values()],
                marker_color=["#7C6CF6", "#F669C1"],
                text=[f"{v['accuracy']*100:.1f}%" for v in eval_results.values()],
                textposition="outside",
            )
        )
        fig.update_layout(
            title="Top-1 Accuracy (%)", height=320, plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
            font=dict(color="#2D2A45"), yaxis=dict(gridcolor="#F0EDFF"),
        )
        st.plotly_chart(fig, width="stretch")

    st.markdown("#### ⚖️ Model Size Comparison")
    fig = go.Figure(
        go.Bar(
            x=list(eval_results.keys()),
            y=[v["params"] for v in eval_results.values()],
            marker_color=["#6CD4F6", "#F6C86C"],
            text=[f"{v['params']:,}" for v in eval_results.values()],
            textposition="outside",
        )
    )
    fig.update_layout(
        height=300, plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        font=dict(color="#2D2A45"), yaxis=dict(title="Trainable parameters", gridcolor="#F0EDFF"),
    )
    st.plotly_chart(fig, width="stretch")

    st.markdown("#### 🔠 Top 20 Most Frequent Words")
    common = word_counts.most_common(20)
    fig = px.bar(
        x=[c for _, c in common][::-1], y=[w for w, _ in common][::-1], orientation="h",
        color=[c for _, c in common][::-1], color_continuous_scale=[[0, "#FDE2F1"], [1, "#F669C1"]],
    )
    fig.update_layout(
        height=460, plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", showlegend=False,
        coloraxis_showscale=False, font=dict(color="#2D2A45"),
        xaxis=dict(title="Frequency", gridcolor="#F0EDFF"), yaxis=dict(title=""),
    )
    st.plotly_chart(fig, width="stretch")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("#### 📏 Quote Length Distribution")
        fig = px.histogram(lengths[lengths <= 80], nbins=40, color_discrete_sequence=["#A98CF9"])
        fig.update_layout(
            height=360, plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", showlegend=False,
            font=dict(color="#2D2A45"), xaxis=dict(title="Words per quote", gridcolor="#F0EDFF"),
            yaxis=dict(title="Count", gridcolor="#F0EDFF"),
        )
        st.plotly_chart(fig, width="stretch")
    with c4:
        st.markdown("#### ✍️ Top 10 Authors")
        fig = px.bar(
            x=top_authors.values, y=top_authors.index, orientation="h",
            color=top_authors.values, color_continuous_scale=[[0, "#DDEBFF"], [1, "#6CD4F6"]],
        )
        fig.update_layout(
            height=360, plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF", showlegend=False,
            coloraxis_showscale=False, font=dict(color="#2D2A45"),
            xaxis=dict(title="Number of quotes", gridcolor="#F0EDFF"), yaxis=dict(title=""),
        )
        st.plotly_chart(fig, width="stretch")

    st.markdown("#### 📉 Zipf's Law (word rank vs. frequency)")
    freqs = sorted(word_counts.values(), reverse=True)
    fig = go.Figure(go.Scatter(x=list(range(1, len(freqs) + 1)), y=freqs, mode="lines", line=dict(color="#7C6CF6", width=3)))
    fig.update_layout(
        height=360, plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        font=dict(color="#2D2A45"),
        xaxis=dict(title="Word rank (log scale)", type="log", gridcolor="#F0EDFF"),
        yaxis=dict(title="Frequency (log scale)", type="log", gridcolor="#F0EDFF"),
    )
    st.plotly_chart(fig, width="stretch")

# ==========================================================================
# TAB 3 -- About
# ==========================================================================
with tab_about:
    st.markdown('<div class="fade-card">', unsafe_allow_html=True)
    st.markdown(
        """
#### How it works
1. **Data** — ~3,000 famous quotes are lowercased and stripped of punctuation.
2. **Vocabulary** — the 10,000 most frequent words are mapped to integer ids (built with a plain Python `Counter`, since PyTorch has no built-in `Tokenizer`).
3. **Training pairs** — every quote is turned into growing `(words-so-far → next word)` examples.
4. **Models** — an `Embedding → RNN/LSTM → Linear` network is trained from scratch in PyTorch for each architecture.
5. **Inference** — this app loads the already-trained weights (`models/rnn_model.pth`, `models/lstm_model.pth`) and only ever runs a forward pass — no training happens inside the app.

#### Tech stack
- **PyTorch** — model definition, training (in the notebook) and inference
- **Streamlit** — interactive web app
- **Plotly** — interactive, animated charts
- **Pandas / NumPy** — data handling

#### Project structure
```
Sentence Auto Completer Bot/
├── app.py                  ← this Streamlit app
├── requirements.txt
├── models/                 ← trained weights + vocabulary
├── data/                   ← quotes dataset
├── notebook/                ← full training / evaluation notebook
├── graphs/                 ← training curves & analysis charts
└── preview/                 ← screenshots & demo video
```
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)
