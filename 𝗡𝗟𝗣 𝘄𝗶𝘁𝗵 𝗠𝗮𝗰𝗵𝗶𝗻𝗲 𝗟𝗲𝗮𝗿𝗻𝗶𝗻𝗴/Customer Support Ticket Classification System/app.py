"""
Customer Support Ticket Classification System
================================================
A production-style Streamlit application that classifies incoming customer
support tickets into a CATEGORY (e.g. ORDER, REFUND, ACCOUNT) and a specific
INTENT (e.g. cancel_order, track_refund) using TF-IDF + LinearSVC pipelines
trained offline (see notebook/Customer Support Ticket Classification.ipynb).

Run with:
    streamlit run app.py
"""

import json
import re
import string
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

# --------------------------------------------------------------------------
# Portable paths (never hardcode machine-specific paths)
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
GRAPH_DIR = BASE_DIR / "graphs"
DATA_DIR = BASE_DIR / "data"

# --------------------------------------------------------------------------
# Page configuration
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Customer Support Ticket Classifier",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# Custom CSS — restrained, professional "AI product" look
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .main .block-container {padding-top: 2rem; padding-bottom: 3rem;}

        .hero {
            padding: 2rem 2.2rem;
            border-radius: 14px;
            background: linear-gradient(135deg, #101828 0%, #1d2b4f 100%);
            color: #ffffff;
            margin-bottom: 1.6rem;
        }
        .hero h1 {
            font-size: 2.05rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
            color: #ffffff;
        }
        .hero p {
            font-size: 1.02rem;
            color: #cbd5e1;
            margin-bottom: 0.2rem;
        }
        .hero .tag {
            display: inline-block;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.18);
            padding: 0.25rem 0.7rem;
            border-radius: 999px;
            font-size: 0.8rem;
            color: #e2e8f0;
            margin-top: 0.7rem;
        }

        div[data-testid="stMetric"] {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 0.9rem 1rem 0.6rem 1rem;
        }

        .result-card {
            border-radius: 12px;
            padding: 1.3rem 1.5rem;
            border: 1px solid #e2e8f0;
            background: #f8fafc;
            margin-bottom: 0.8rem;
        }
        .result-card .label {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #64748b;
            font-weight: 600;
        }
        .result-card .value {
            font-size: 1.55rem;
            font-weight: 700;
            color: #101828;
            margin-top: 0.15rem;
        }
        .result-card .conf {
            font-size: 0.9rem;
            color: #16a34a;
            font-weight: 600;
            margin-top: 0.3rem;
        }

        .cleaned-box {
            background: #0f172a;
            color: #a7f3d0;
            font-family: 'Courier New', monospace;
            font-size: 0.88rem;
            padding: 0.8rem 1rem;
            border-radius: 8px;
            overflow-x: auto;
        }

        section[data-testid="stSidebar"] {
            border-right: 1px solid #e2e8f0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Text preprocessing — MUST match training exactly (notebook cell defining
# clean_text). Do not alter this logic; it must stay consistent with what
# the saved TF-IDF vectorizers were fitted on.
# --------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_nltk_resources():
    import nltk

    for pkg, path in [
        ("stopwords", "corpora/stopwords"),
        ("wordnet", "corpora/wordnet"),
        ("omw-1.4", "corpora/omw-1.4"),
    ]:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg, quiet=True)

    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))
    keep_words = {
        "no", "not", "nor", "why", "how", "when", "where", "what",
        "can", "cannot", "don't", "can't", "won't",
    }
    stop_words = stop_words - keep_words
    return lemmatizer, stop_words


LEMMATIZER, STOP_WORDS = load_nltk_resources()


def clean_text(text: str) -> str:
    """Identical preprocessing to the training notebook."""
    text = text.lower()
    text = re.sub(r"\{\{.*?\}\}", " ", text)
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = text.split()
    tokens = [LEMMATIZER.lemmatize(tok) for tok in tokens if tok not in STOP_WORDS]
    return " ".join(tokens)


# --------------------------------------------------------------------------
# Cached loaders for models / metadata (loaded once per session)
# --------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_models():
    category_pipeline = joblib.load(MODEL_DIR / "category_pipeline.pkl")
    intent_pipeline = joblib.load(MODEL_DIR / "intent_pipeline.pkl")
    category_encoder = joblib.load(MODEL_DIR / "category_label_encoder.pkl")
    intent_encoder = joblib.load(MODEL_DIR / "intent_label_encoder.pkl")
    return category_pipeline, intent_pipeline, category_encoder, intent_encoder


@st.cache_data(show_spinner=False)
def load_json(filename):
    path = MODEL_DIR / filename
    if not path.exists():
        return None
    with open(path, "r") as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_model_comparison():
    path = MODEL_DIR / "model_comparison.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_dataset_sample(n=2000):
    path = DATA_DIR / "customer_dataset_raw.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if len(df) > n:
        df = df.sample(n, random_state=42)
    return df


try:
    category_pipeline, intent_pipeline, category_encoder, intent_encoder = load_models()
    MODELS_LOADED = True
    MODEL_LOAD_ERROR = None
except Exception as e:  # noqa: BLE001
    MODELS_LOADED = False
    MODEL_LOAD_ERROR = str(e)

category_report = load_json("category_eval_report.json")
intent_report = load_json("intent_eval_report.json")
model_comparison_df = load_model_comparison()


def decision_confidence(pipeline, cleaned_text: str, top_k: int = 3):
    """
    LinearSVC does not expose predict_proba. We derive a normalized
    confidence score from the decision_function margins via softmax so the
    UI can show a relative confidence ranking. This is NOT a calibrated
    probability — it is explicitly labeled "confidence score" in the UI.
    """
    scores = pipeline.decision_function([cleaned_text])[0]
    scores = np.atleast_1d(scores)
    exp_scores = np.exp(scores - np.max(scores))
    probs = exp_scores / exp_scores.sum()
    top_idx = np.argsort(probs)[::-1][:top_k]
    return top_idx, probs


# --------------------------------------------------------------------------
# Sidebar navigation
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎫 Navigation")
    page = st.radio(
        "Go to",
        ["🏠 Prediction", "📊 Analytics", "🧠 Model Insights", "📖 About"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        """
        **Model stack**
        - TF-IDF (1–2 grams, 20k features)
        - LinearSVC classifiers
        - Separate pipelines for Category & Intent

        **Dataset**
        - ~26.9k labeled support tickets
        - 11 categories · 27 intents
        """
    )
    st.markdown("---")
    st.caption("Built with Python · scikit-learn · Streamlit")


# ==========================================================================
# PAGE: PREDICTION
# ==========================================================================
if page == "🏠 Prediction":
    st.markdown(
        """
        <div class="hero">
            <h1>🤖 Customer Support Ticket Classifier</h1>
            <p>Automatically route incoming support tickets by predicting their
            <b>category</b> and <b>customer intent</b> from raw text.</p>
            <span class="tag">TF-IDF + LinearSVC</span>
            <span class="tag">11 Categories</span>
            <span class="tag">27 Intents</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not MODELS_LOADED:
        st.error(
            "Model artifacts could not be loaded. Please verify the `models/` "
            f"folder is present next to app.py.\n\nDetails: {MODEL_LOAD_ERROR}"
        )
        st.stop()

    col_input, col_examples = st.columns([2.2, 1])

    with col_examples:
        st.markdown("**Try an example**")
        examples = [
            "I want to cancel my order and get a refund as soon as possible",
            "How do I change the shipping address for my recent purchase?",
            "I need to speak with a human agent about a billing issue",
            "Can you help me recover my account password, I'm locked out",
            "I'd like to leave a review for the product I purchased",
        ]
        for ex in examples:
            if st.button(ex, key=ex, use_container_width=True):
                st.session_state["ticket_text"] = ex

    with col_input:
        ticket_text = st.text_area(
            "Enter the customer support ticket text",
            key="ticket_text",
            height=160,
            placeholder="e.g. 'I ordered a product two weeks ago and it still hasn't "
            "arrived. Can you tell me where my package is?'",
        )
        predict_clicked = st.button("🔍 Classify Ticket", type="primary", use_container_width=True)

    if predict_clicked:
        raw_text = (ticket_text or "").strip()
        if not raw_text:
            st.warning("Please enter some ticket text before classifying.")
        elif len(raw_text) < 3:
            st.warning("The input text is too short to classify meaningfully.")
        else:
            with st.spinner("Analyzing ticket..."):
                cleaned = clean_text(raw_text)

                if not cleaned:
                    st.warning(
                        "After cleaning, no meaningful text remained (input may have "
                        "been only numbers, punctuation, or stopwords). Please provide "
                        "more descriptive ticket text."
                    )
                else:
                    try:
                        cat_top_idx, cat_probs = decision_confidence(category_pipeline, cleaned)
                        int_top_idx, int_probs = decision_confidence(intent_pipeline, cleaned)

                        cat_pred_label = category_encoder.inverse_transform([cat_top_idx[0]])[0]
                        int_pred_label = intent_encoder.inverse_transform([int_top_idx[0]])[0]
                        cat_conf = cat_probs[cat_top_idx[0]]
                        int_conf = int_probs[int_top_idx[0]]
                    except Exception as e:  # noqa: BLE001
                        st.error(f"Prediction failed: {e}")
                        st.stop()

                    st.markdown("### 🔮 Prediction Result")
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.markdown(
                            f"""
                            <div class="result-card">
                                <div class="label">Predicted Category</div>
                                <div class="value">{cat_pred_label}</div>
                                <div class="conf">Confidence score: {cat_conf:.1%}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    with res_col2:
                        st.markdown(
                            f"""
                            <div class="result-card">
                                <div class="label">Predicted Intent</div>
                                <div class="value">{int_pred_label}</div>
                                <div class="conf">Confidence score: {int_conf:.1%}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with st.expander("🔎 See top-3 predictions & cleaned text"):
                        t1, t2 = st.columns(2)
                        with t1:
                            st.markdown("**Top categories**")
                            cat_labels_top = category_encoder.inverse_transform(cat_top_idx)
                            for lbl, idx in zip(cat_labels_top, cat_top_idx):
                                st.progress(float(cat_probs[idx]), text=f"{lbl} — {cat_probs[idx]:.1%}")
                        with t2:
                            st.markdown("**Top intents**")
                            int_labels_top = intent_encoder.inverse_transform(int_top_idx)
                            for lbl, idx in zip(int_labels_top, int_top_idx):
                                st.progress(float(int_probs[idx]), text=f"{lbl} — {int_probs[idx]:.1%}")

                        st.markdown("**Cleaned text fed to the model**")
                        st.markdown(f'<div class="cleaned-box">{cleaned}</div>', unsafe_allow_html=True)

                    st.info(
                        "Confidence scores are derived from LinearSVC decision-function "
                        "margins via softmax normalization — they indicate relative "
                        "model certainty, not calibrated probabilities.",
                        icon="ℹ️",
                    )


# ==========================================================================
# PAGE: ANALYTICS
# ==========================================================================
elif page == "📊 Analytics":
    st.markdown(
        """
        <div class="hero">
            <h1>📊 Dataset Analytics</h1>
            <p>Exploratory insights from the ~26.9k labeled customer support tickets
            used to train the models.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df_sample = load_dataset_sample()

    if df_sample is not None:
        m1, m2, m3, m4 = st.columns(4)
        full_len = None
        try:
            full_len = sum(1 for _ in open(DATA_DIR / "customer_dataset_raw.csv")) - 1
        except Exception:  # noqa: BLE001
            full_len = len(df_sample)
        m1.metric("Total Tickets", f"{full_len:,}")
        m2.metric("Categories", df_sample["category"].nunique())
        m3.metric("Intents", df_sample["intent"].nunique())
        m4.metric("Avg. Words / Ticket", f"{df_sample['instruction'].astype(str).str.split().apply(len).mean():.1f}")

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["Category Distribution", "Intent Distribution", "Text Length"])

    with tab1:
        img = GRAPH_DIR / "category_distribution.png"
        if img.exists():
            st.image(str(img), use_container_width=True)
        else:
            st.warning("Graph not found: category_distribution.png")

    with tab2:
        img = GRAPH_DIR / "intent_distribution.png"
        if img.exists():
            st.image(str(img), use_container_width=True)
        else:
            st.warning("Graph not found: intent_distribution.png")

    with tab3:
        img = GRAPH_DIR / "text_length_distribution.png"
        if img.exists():
            st.image(str(img), use_container_width=True)
        else:
            st.warning("Graph not found: text_length_distribution.png")

    if df_sample is not None:
        with st.expander("🔍 Browse a sample of the dataset"):
            st.dataframe(
                df_sample[["instruction", "category", "intent"]].reset_index(drop=True),
                use_container_width=True,
                height=320,
            )


# ==========================================================================
# PAGE: MODEL INSIGHTS
# ==========================================================================
elif page == "🧠 Model Insights":
    st.markdown(
        """
        <div class="hero">
            <h1>🧠 Model Performance & Insights</h1>
            <p>How the final models were selected and how they perform on the held-out test set.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if category_report and intent_report:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Category Accuracy", f"{category_report['accuracy']:.2%}")
        m2.metric("Category Macro-F1", f"{category_report['macro avg']['f1-score']:.2%}")
        m3.metric("Intent Accuracy", f"{intent_report['accuracy']:.2%}")
        m4.metric("Intent Macro-F1", f"{intent_report['macro avg']['f1-score']:.2%}")

    st.markdown("---")
    st.markdown("#### 🏆 Model Comparison (validation results)")
    if model_comparison_df is not None:
        st.dataframe(
            model_comparison_df.style.format(
                {"accuracy": "{:.4f}", "f1_macro": "{:.4f}", "f1_weighted": "{:.4f}"}
            ),
            use_container_width=True,
        )
        img = GRAPH_DIR / "model_comparison.png"
        if img.exists():
            st.image(str(img), use_container_width=True)
    else:
        st.warning("model_comparison.csv not found.")

    st.markdown("---")
    st.markdown("#### 📈 Confusion Matrices & Per-Class Performance")
    tab1, tab2, tab3 = st.tabs(["Category Confusion Matrix", "Intent Confusion Matrix", "Per-Category F1"])

    with tab1:
        img = GRAPH_DIR / "category_confusion_matrix.png"
        if img.exists():
            st.image(str(img), use_container_width=True)
        else:
            st.warning("Graph not found: category_confusion_matrix.png")

    with tab2:
        img = GRAPH_DIR / "intent_confusion_matrix.png"
        if img.exists():
            st.image(str(img), use_container_width=True)
        else:
            st.warning("Graph not found: intent_confusion_matrix.png")

    with tab3:
        img = GRAPH_DIR / "category_f1_scores.png"
        if img.exists():
            st.image(str(img), use_container_width=True)
        else:
            st.warning("Graph not found: category_f1_scores.png")

    st.markdown("---")
    st.markdown("#### 📋 Full Classification Reports")
    rcol1, rcol2 = st.columns(2)
    with rcol1:
        st.markdown("**Category classifier**")
        if category_report:
            rep_df = pd.DataFrame(category_report).T
            rep_df = rep_df[~rep_df.index.isin(["accuracy"])]
            st.dataframe(rep_df.style.format("{:.3f}"), use_container_width=True, height=300)
    with rcol2:
        st.markdown("**Intent classifier**")
        if intent_report:
            rep_df = pd.DataFrame(intent_report).T
            rep_df = rep_df[~rep_df.index.isin(["accuracy"])]
            st.dataframe(rep_df.style.format("{:.3f}"), use_container_width=True, height=300)

    st.markdown("---")
    st.markdown(
        """
        #### Why TF-IDF + LinearSVC?
        Both Bag-of-Words and TF-IDF features were tested against Multinomial Naive
        Bayes, Logistic Regression, and LinearSVC. **TF-IDF (1–2 grams, 20,000
        features) combined with LinearSVC** produced the best validation accuracy
        and macro-F1 for *both* the category and intent targets, so it was selected
        as the final model for each task and re-trained on train+validation data
        before being evaluated once on the held-out test set.

        **Limitations:** the model is a linear text classifier — it can struggle
        with sarcasm, multi-intent tickets, or phrasing far outside the training
        distribution (which is templated customer-support language). LinearSVC
        also does not produce calibrated probabilities; confidence scores shown in
        the app are relative, softmax-normalized decision-function margins.
        """
    )


# ==========================================================================
# PAGE: ABOUT
# ==========================================================================
elif page == "📖 About":
    st.markdown(
        """
        <div class="hero">
            <h1>📖 About This Project</h1>
            <p>Customer Support Ticket Classification System</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        #### 🎯 Objective
        Automatically classify incoming customer support tickets by **category**
        (e.g. ORDER, REFUND, ACCOUNT) and **intent** (e.g. `cancel_order`,
        `track_refund`) to support automated ticket routing and triage.

        #### 📂 Dataset
        ~26.9k labeled customer-support instructions spanning **11 categories**
        and **27 fine-grained intents**, with columns for the customer message
        (`instruction`), its `category`, `intent`, and an example agent
        `response`.

        #### 🔬 Methodology
        1. **Text cleaning** — lowercasing, placeholder/URL removal, punctuation
           and digit stripping, stopword removal (keeping negation/question
           words), and lemmatization.
        2. **Feature extraction** — Bag-of-Words and TF-IDF (1–2 grams, 20,000
           max features) were both evaluated.
        3. **Modeling** — Multinomial Naive Bayes, Logistic Regression, and
           LinearSVC were trained and compared for each target (category,
           intent) across both feature sets — 12 combinations total.
        4. **Model selection** — TF-IDF + LinearSVC won on validation accuracy
           and macro-F1 for both targets.
        5. **Evaluation** — final pipelines evaluated once on a held-out test
           split; full classification reports and confusion matrices saved.

        #### 🧰 Technologies
        Python · pandas · scikit-learn · NLTK · Matplotlib · Seaborn ·
        Streamlit · joblib

        #### ⚠️ Limitations
        - Predictions reflect patterns in a templated customer-support dataset
          and may not generalize to very different writing styles.
        - Confidence scores are relative (softmax over SVM decision margins),
          not calibrated probabilities.
        - The model classifies a single ticket at a time and assumes one
          dominant intent per message.

        #### 🚀 Future Improvements
        - Add a transformer-based classifier (e.g. DistilBERT) for comparison.
        - Multi-label support for tickets with more than one intent.
        - Active-learning loop to continuously improve on misrouted tickets.
        """
    )

    st.markdown("---")
    st.caption("Built as part of an AI/ML portfolio project.")
