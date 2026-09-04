"""
ChatGPT Sentiment Analysis — Streamlit application.

Run with:
    streamlit run app.py

This app wraps the existing trained scikit-learn models (Logistic
Regression on Bag-of-Words and on TF-IDF features) that were produced in
notebooks/ChatGPT Sentiment Analysis using NLP & Machine Learning.ipynb,
and exposes them through a polished, production-style UI.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

# Make sure `utils` is importable regardless of the working directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils.preprocessing import clean_text, clean_series
from utils.model_loader import (
    DISPLAY_META,
    LABEL_ORDER,
    data_file_path,
    load_bundle,
    load_confusion_matrix,
    load_eval_report,
)

# --------------------------------------------------------------------------
# Page configuration
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="ChatGPT Sentiment Analysis",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .app-header {
        padding: 1.75rem 2rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #10131f 0%, #1b2140 100%);
        color: #ffffff;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .app-header h1 {
        margin: 0;
        font-size: 1.9rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .app-header p {
        margin: 0.4rem 0 0 0;
        color: rgba(255,255,255,0.72);
        font-size: 0.98rem;
    }
    .app-header .badge-row {
        margin-top: 0.85rem;
    }
    .badge {
        display: inline-block;
        padding: 0.22rem 0.65rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.14);
        color: rgba(255,255,255,0.85);
        font-size: 0.76rem;
        font-weight: 600;
        margin-right: 0.4rem;
    }

    .card {
        border-radius: 14px;
        border: 1px solid rgba(120,120,140,0.18);
        background: rgba(127,127,127,0.04);
        padding: 1.25rem 1.4rem;
        margin-bottom: 1rem;
    }

    .result-card {
        border-radius: 16px;
        padding: 1.6rem 1.8rem;
        border: 1px solid rgba(120,120,140,0.18);
        margin-top: 0.5rem;
    }
    .result-label {
        font-size: 1.6rem;
        font-weight: 800;
        margin: 0;
    }
    .result-sub {
        color: rgba(140,140,160,0.9);
        font-size: 0.92rem;
        margin-top: 0.15rem;
    }

    .section-title {
        font-weight: 800;
        font-size: 1.15rem;
        margin: 0.2rem 0 0.8rem 0;
        letter-spacing: -0.01em;
    }

    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.3rem;
        border: none;
    }
    .stButton>button:first-child {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: white;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <h1>💬 ChatGPT Sentiment Analysis</h1>
        <p>NLP-powered classifier that reads a tweet about ChatGPT and tells you
        whether the sentiment behind it is positive, negative, or neutral.</p>
        <div class="badge-row">
            <span class="badge">🧠 Logistic Regression</span>
            <span class="badge">🔤 Bag-of-Words / TF-IDF</span>
            <span class="badge">🐍 scikit-learn</span>
            <span class="badge">📊 85.6% test accuracy</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------
# Cached resource / data loaders
# --------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading model...")
def get_bundle(kind: str):
    return load_bundle(kind)


@st.cache_data(show_spinner=False)
def get_eval_report():
    return load_eval_report()


@st.cache_data(show_spinner=False)
def get_confusion_matrix():
    cm = load_confusion_matrix()
    return cm.tolist() if cm is not None else None


@st.cache_data(show_spinner="Reading dataset...")
def get_label_distribution():
    """Class distribution straight from the original labeled dataset."""
    path = data_file_path("file.csv")
    if not path.exists():
        return None
    df = pd.read_csv(path, usecols=["labels"])
    counts = df["labels"].value_counts().reindex(LABEL_ORDER).fillna(0).astype(int)
    return counts


@st.cache_data(show_spinner=False)
def clean_text_cached(text: str) -> str:
    return clean_text(text)


@st.cache_data(show_spinner="Scoring rows...")
def predict_dataframe(_bundle, texts: pd.Series):
    cleaned = clean_series(texts)
    vecs = _bundle.vectorizer.transform(cleaned)
    preds = _bundle.model.predict(vecs)
    labels = [LABEL_ORDER[int(p)] for p in preds]

    result = pd.DataFrame({"text": texts, "cleaned_text": cleaned, "predicted_sentiment": labels})

    if hasattr(_bundle.model, "predict_proba"):
        probs = _bundle.model.predict_proba(vecs)
        # build probability columns in fixed LABEL_ORDER
        class_to_col = {int(c): i for i, c in enumerate(_bundle.model.classes_)}
        for label in LABEL_ORDER:
            label_idx = LABEL_ORDER.index(label)
            if label_idx in class_to_col:
                result[f"confidence_{label}"] = probs[:, class_to_col[label_idx]]
    return result


# --------------------------------------------------------------------------
# Sidebar — model selection (shared across tabs)
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Model settings")
    model_choice = st.radio(
        "Vectorizer + Model",
        options=["bow", "tfidf"],
        format_func=lambda k: "Bag-of-Words (primary)" if k == "bow" else "TF-IDF (comparison)",
        index=0,
        help="Both were trained as Logistic Regression classifiers on the same "
        "cleaned tweets. The Bag-of-Words model is the one the evaluation "
        "report / confusion matrix were generated from.",
    )
    st.caption(
        "Swap the vectorizer to compare predictions. The BoW model is the "
        "primary, benchmarked model for this project."
    )

    st.markdown("---")
    st.markdown("### 🏷️ Sentiment classes")
    for label in LABEL_ORDER:
        meta = DISPLAY_META[label]
        st.markdown(f"{meta['emoji']} **{meta['text']}**")

try:
    bundle = get_bundle(model_choice)
    load_error = None
except Exception as e:  # noqa: BLE001
    bundle = None
    load_error = str(e)

if load_error:
    st.error(f"⚠️ Could not load the model: {load_error}")
    st.stop()


# --------------------------------------------------------------------------
# Tabs
# --------------------------------------------------------------------------
tab_predict, tab_batch, tab_perf, tab_about = st.tabs(
    ["🔮 Predict", "📁 Batch Analysis", "📊 Model Performance", "ℹ️ About"]
)

# ============================== PREDICT TAB ==============================
with tab_predict:
    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.markdown('<p class="section-title">Analyze a tweet</p>', unsafe_allow_html=True)

        examples = {
            "— pick an example —": "",
            "Positive example": "ChatGPT has completely changed how I write my essays, it's incredible and so helpful!",
            "Negative example": "ChatGPT gave me a completely wrong answer again, this thing is so unreliable and frustrating.",
            "Neutral example": "ChatGPT: Optimizing Language Models for Dialogue https://t.co/K9rKRygYyn @OpenAI",
        }
        chosen_example = st.selectbox("Quick examples", list(examples.keys()), label_visibility="collapsed")

        default_text = examples[chosen_example] if chosen_example != "— pick an example —" else ""
        user_text = st.text_area(
            "Tweet text",
            value=default_text,
            height=150,
            placeholder="Type or paste a tweet about ChatGPT here...",
            label_visibility="collapsed",
        )

        analyze_clicked = st.button("🔍 Analyze sentiment", type="primary", width='stretch')

    with right:
        st.markdown('<p class="section-title">Result</p>', unsafe_allow_html=True)

        if analyze_clicked:
            if not user_text or not user_text.strip():
                st.warning("Please enter some text to analyze.")
            else:
                cleaned = clean_text_cached(user_text)
                if not cleaned:
                    st.warning(
                        "After cleaning (removing punctuation, links, and stopwords), "
                        "there's no meaningful text left to classify. Try a longer tweet."
                    )
                else:
                    pred_label, probs = bundle.predict(cleaned)
                    meta = DISPLAY_META[pred_label]

                    confidence = probs[pred_label] if probs else None

                    st.markdown(
                        f"""
                        <div class="result-card" style="background: {meta['color']}14; border-color: {meta['color']}55;">
                            <p class="result-label" style="color:{meta['color']};">{meta['emoji']} {meta['text']}</p>
                            <p class="result-sub">Predicted class: <b>{pred_label}</b>{f" &nbsp;•&nbsp; Confidence: <b>{confidence*100:.1f}%</b>" if confidence is not None else ""}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if probs:
                        st.markdown("&nbsp;", unsafe_allow_html=True)
                        prob_df = pd.DataFrame(
                            {
                                "Sentiment": [DISPLAY_META[l]["text"] for l in LABEL_ORDER],
                                "Probability": [probs.get(l, 0.0) for l in LABEL_ORDER],
                            }
                        ).set_index("Sentiment")
                        st.bar_chart(prob_df, height=220)

                    with st.expander("🧪 See preprocessing details"):
                        st.markdown(f"**Model used:** {bundle.display_name}")
                        st.markdown("**Original text:**")
                        st.code(user_text, language=None)
                        st.markdown("**Cleaned text fed to the model:**")
                        st.code(cleaned, language=None)
        else:
            st.info("Enter a tweet on the left and click **Analyze sentiment** to see the prediction here.")


# ============================== BATCH TAB =================================
with tab_batch:
    st.markdown('<p class="section-title">Batch analysis from a CSV file</p>', unsafe_allow_html=True)
    st.caption(
        "Upload a CSV containing a column of tweets/text. Each row will be cleaned "
        "and classified with the currently selected model."
    )

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

    if uploaded_file is not None:
        try:
            batch_df = pd.read_csv(uploaded_file)
        except Exception as e:  # noqa: BLE001
            st.error(f"Could not read this CSV: {e}")
            batch_df = None

        if batch_df is not None and not batch_df.empty:
            col1, col2 = st.columns([2, 1])
            with col1:
                text_col = st.selectbox("Which column contains the text to analyze?", batch_df.columns.tolist())
            with col2:
                max_rows = st.number_input(
                    "Max rows to process",
                    min_value=1,
                    max_value=int(len(batch_df)),
                    value=int(min(500, len(batch_df))),
                    step=50,
                    help="Limits processing time for very large files.",
                )

            run_batch = st.button("🚀 Run batch prediction", type="primary")

            if run_batch:
                subset = batch_df.head(int(max_rows)).copy()
                subset[text_col] = subset[text_col].astype(str)

                with st.spinner("Running predictions..."):
                    results = predict_dataframe(bundle, subset[text_col])

                st.success(f"Scored {len(results)} rows with {bundle.display_name}.")

                m1, m2, m3 = st.columns(3)
                dist = results["predicted_sentiment"].value_counts().reindex(LABEL_ORDER).fillna(0).astype(int)
                for col, label in zip((m1, m2, m3), LABEL_ORDER):
                    meta = DISPLAY_META[label]
                    col.metric(f"{meta['emoji']} {meta['text']}", int(dist.get(label, 0)))

                st.markdown("**Predicted sentiment distribution**")
                st.bar_chart(dist.rename(index=lambda l: DISPLAY_META[l]["text"]))

                st.markdown("**Results**")
                st.dataframe(results, width='stretch', height=360)

                st.download_button(
                    "⬇️ Download results as CSV",
                    data=results.to_csv(index=False).encode("utf-8"),
                    file_name="sentiment_predictions.csv",
                    mime="text/csv",
                )
        elif batch_df is not None:
            st.warning("The uploaded file appears to be empty.")
    else:
        st.info("Upload a CSV file to get started, or try the single-tweet **Predict** tab.")


# ============================ PERFORMANCE TAB ==============================
with tab_perf:
    st.markdown('<p class="section-title">Model performance (Logistic Regression + Bag-of-Words)</p>', unsafe_allow_html=True)
    st.caption("Computed on a held-out 20% test split of the labeled dataset (43,859 tweets).")

    report = get_eval_report()
    cm = get_confusion_matrix()

    if report:
        acc = report.get("accuracy")
        macro_f1 = report.get("macro avg", {}).get("f1-score")
        weighted_f1 = report.get("weighted avg", {}).get("f1-score")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Accuracy", f"{acc*100:.1f}%")
        m2.metric("Macro F1", f"{macro_f1:.3f}")
        m3.metric("Weighted F1", f"{weighted_f1:.3f}")
        m4.metric("Test samples", f"{int(report.get('macro avg', {}).get('support', 0)):,}")

        st.markdown("&nbsp;")
        c1, c2 = st.columns([1.1, 1], gap="large")

        with c1:
            st.markdown("**Per-class metrics**")
            rows = []
            for label in LABEL_ORDER:
                r = report.get(label, {})
                rows.append(
                    {
                        "Class": DISPLAY_META[label]["text"],
                        "Precision": round(r.get("precision", 0), 3),
                        "Recall": round(r.get("recall", 0), 3),
                        "F1-score": round(r.get("f1-score", 0), 3),
                        "Support": int(r.get("support", 0)),
                    }
                )
            st.dataframe(pd.DataFrame(rows).set_index("Class"), width='stretch')

        with c2:
            st.markdown("**Confusion matrix**")
            if cm:
                cm_df = pd.DataFrame(
                    cm,
                    index=[f"Actual: {DISPLAY_META[l]['text']}" for l in LABEL_ORDER],
                    columns=[f"Pred: {DISPLAY_META[l]['text']}" for l in LABEL_ORDER],
                )
                st.dataframe(
                    cm_df.style.background_gradient(cmap="Blues", axis=None),
                    width='stretch',
                )
            else:
                st.info("Confusion matrix artifact not found.")
    else:
        st.info("No evaluation report found in `models/eval_report.json`.")


# ============================== ABOUT TAB ==================================
with tab_about:
    c1, c2 = st.columns([1.3, 1], gap="large")

    with c1:
        st.markdown('<p class="section-title">About this project</p>', unsafe_allow_html=True)
        st.markdown(
            """
This app classifies tweets that mention **ChatGPT** into three sentiment
classes — **positive**, **negative**, or **neutral** — using a classic NLP +
machine learning pipeline trained from scratch on a labeled Twitter dataset.

**How it works**
1. **Clean** — the raw tweet is lowercased, stripped of punctuation, links
   are removed, and common English stopwords are dropped (negation words
   like *no / not / never* are deliberately kept, since they flip meaning).
2. **Vectorize** — the cleaned text is converted into numeric features
   using either a **Bag-of-Words** (`CountVectorizer`) or **TF-IDF**
   (`TfidfVectorizer`) representation, fit on the training vocabulary.
3. **Classify** — a **Logistic Regression** model, trained on those
   features, predicts one of the three sentiment classes and a confidence
   score for each class.

**Tech stack**
- Python, scikit-learn, pandas, NumPy
- `CountVectorizer` / `TfidfVectorizer` for feature extraction
- `LogisticRegression` for classification
- Streamlit for the interface

**Limitations**
- Trained only on English-language tweets about ChatGPT — may not
  generalize well to other topics, languages, or much longer text.
- Bag-of-Words / TF-IDF + Logistic Regression cannot capture sarcasm,
  complex negation across long sentences, or deep context the way modern
  transformer-based models can.
- Class balance in the source data is uneven (see distribution chart),
  which can bias predictions toward the majority class in ambiguous cases.
            """
        )

    with c2:
        st.markdown('<p class="section-title">Dataset class distribution</p>', unsafe_allow_html=True)
        dist = get_label_distribution()
        if dist is not None:
            st.bar_chart(dist.rename(index=lambda l: DISPLAY_META[l]["text"]))
            st.caption(f"{int(dist.sum()):,} labeled tweets total.")
        else:
            st.info("Dataset file not found — showing model metrics only.")

        st.markdown("&nbsp;")
        st.markdown('<p class="section-title">Usage tips</p>', unsafe_allow_html=True)
        st.markdown(
            """
- Use the **Predict** tab for a single tweet.
- Use **Batch Analysis** to score a whole CSV of tweets at once.
- Switch between the **Bag-of-Words** and **TF-IDF** models in the
  sidebar to compare predictions.
            """
        )
