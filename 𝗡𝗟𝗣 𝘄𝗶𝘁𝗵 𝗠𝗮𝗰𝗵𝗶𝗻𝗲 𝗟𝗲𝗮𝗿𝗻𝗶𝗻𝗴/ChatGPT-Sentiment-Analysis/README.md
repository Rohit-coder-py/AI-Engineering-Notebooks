# 💬 ChatGPT Sentiment Analysis

A Streamlit application that classifies tweets about **ChatGPT** as
**positive**, **negative**, or **neutral**, built on a classic NLP + machine
learning pipeline (Bag-of-Words / TF-IDF + Logistic Regression).

## Features

- **Single-tweet prediction** — type or paste a tweet and get an instant
  sentiment label with per-class confidence scores.
- **Batch analysis** — upload a CSV of tweets, pick the text column, and
  score them all at once; view the sentiment distribution and download the
  results.
- **Model performance dashboard** — accuracy, macro/weighted F1, per-class
  precision/recall/F1, and the confusion matrix from the held-out test set.
- **Model comparison** — switch between the Bag-of-Words and TF-IDF
  Logistic Regression models from the sidebar.
- **About / methodology** — explains the cleaning pipeline, tech stack,
  dataset class balance, and known limitations.

## Model & approach

Trained in `notebooks/ChatGPT Sentiment Analysis using NLP & Machine Learning.ipynb`
on ~44K labeled tweets (`neutral`, `good`, `bad`):

1. **Text cleaning** — lowercase → strip punctuation → remove URLs → remove
   English stopwords (keeping negation words `no / not / nor / never`,
   since they flip sentiment meaning).
2. **Feature extraction** — `CountVectorizer` (Bag-of-Words) and
   `TfidfVectorizer` (TF-IDF), each fit on the cleaned training tweets.
3. **Classification** — `LogisticRegression` trained separately on each
   feature set.

The **Bag-of-Words** model is the primary/benchmarked model
(`models/eval_report.json`, `models/confusion_matrix.npy`):

| Metric | Score |
|---|---|
| Accuracy | 85.6% |
| Macro F1 | 0.835 |
| Weighted F1 | 0.854 |

## Tech stack

Python · scikit-learn · pandas · NumPy · Streamlit

## Project structure

```text
.
├── app.py                  # Streamlit entry point
├── requirements.txt
├── utils/
│   ├── preprocessing.py    # exact training-time text cleaning pipeline
│   └── model_loader.py     # cached model/vectorizer/report loading
├── models/
│   ├── bow_vectorizer.pkl / logistic_model_bow.pkl
│   ├── tfidf_vectorizer.pkl / logistic_model_tfidf.pkl
│   ├── label_mapping.json
│   ├── eval_report.json
│   └── confusion_matrix.npy
├── data/
│   ├── file.csv              # raw labeled tweets
│   └── prepared_dataset.csv  # cleaned tweets used for training
└── notebooks/
    └── ChatGPT Sentiment Analysis using NLP & Machine Learning.ipynb
```

## Installation

```bash
pip install -r requirements.txt
```

## Run

From the project folder:

```bash
streamlit run app.py
```

The app works from any working directory — all file paths are resolved
relative to `app.py` itself.

## Limitations

- Trained only on English-language tweets specifically about ChatGPT;
  may not generalize to other topics or much longer text.
- Bag-of-Words / TF-IDF + Logistic Regression can't capture sarcasm or
  deep context the way transformer-based models can.
- The training data's class balance is uneven, which can bias borderline
  predictions toward the majority class.
