"""
Text preprocessing utilities for the ChatGPT Sentiment Analysis app.

IMPORTANT: This mirrors the exact cleaning pipeline used in the training
notebook (notebooks/ChatGPT Sentiment Analysis using NLP & Machine Learning.ipynb)
so that text typed into the app is transformed the same way the training
data was, before it hits the saved BoW / TF-IDF vectorizers.

Pipeline (order matters, matches the notebook cell-by-cell):
    1. Lowercase
    2. Strip punctuation (string.punctuation)
    3. Drop anything from a URL ('https...') onward
    4. Remove English stopwords, EXCEPT negation words
       ('no', 'not', 'nor', 'never') which are kept because they flip
       sentiment meaning.
"""

import string

# Frozen copy of nltk.corpus.stopwords.words("english") (198 words).
# Bundled as a static list so the app never needs a network call / nltk
# download at runtime -- keeps startup fast and fully offline-capable.
_NLTK_ENGLISH_STOPWORDS = [
    "a", "about", "above", "after", "again", "against", "ain", "all", "am",
    "an", "and", "any", "are", "aren", "aren't", "as", "at", "be", "because",
    "been", "before", "being", "below", "between", "both", "but", "by",
    "can", "couldn", "couldn't", "d", "did", "didn", "didn't", "do", "does",
    "doesn", "doesn't", "doing", "don", "don't", "down", "during", "each",
    "few", "for", "from", "further", "had", "hadn", "hadn't", "has", "hasn",
    "hasn't", "have", "haven", "haven't", "having", "he", "he'd", "he'll",
    "he's", "her", "here", "hers", "herself", "him", "himself", "his",
    "how", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is",
    "isn", "isn't", "it", "it'd", "it'll", "it's", "its", "itself", "just",
    "ll", "m", "ma", "me", "mightn", "mightn't", "more", "most", "mustn",
    "mustn't", "my", "myself", "needn", "needn't", "no", "nor", "not",
    "now", "o", "of", "off", "on", "once", "only", "or", "other", "our",
    "ours", "ourselves", "out", "over", "own", "re", "s", "same", "shan",
    "shan't", "she", "she'd", "she'll", "she's", "should", "should've",
    "shouldn", "shouldn't", "so", "some", "such", "t", "than", "that",
    "that'll", "the", "their", "theirs", "them", "themselves", "then",
    "there", "these", "they", "they'd", "they'll", "they're", "they've",
    "this", "those", "through", "to", "too", "under", "until", "up", "ve",
    "very", "was", "wasn", "wasn't", "we", "we'd", "we'll", "we're",
    "we've", "were", "weren", "weren't", "what", "when", "where", "which",
    "while", "who", "whom", "why", "will", "with", "won", "won't",
    "wouldn", "wouldn't", "y", "you", "you'd", "you'll", "you're",
    "you've", "your", "yours", "yourself", "yourselves",
]

_NEGATION_WORDS = {"no", "not", "nor", "never"}
STOP_WORDS = set(_NLTK_ENGLISH_STOPWORDS) - _NEGATION_WORDS

_PUNCT_TABLE = str.maketrans("", "", string.punctuation)


def clean_text(text: str) -> str:
    """Apply the exact training-time cleaning pipeline to a single string."""
    if not isinstance(text, str):
        text = "" if text is None else str(text)

    # 1. lowercase
    text = text.lower()

    # 2. remove punctuation
    text = text.translate(_PUNCT_TABLE)

    # 3. remove URLs / links (everything from 'https' onward)
    text = text.split("https")[0].strip()

    # 4. remove stopwords (keep negations)
    text = " ".join(word for word in text.split() if word not in STOP_WORDS)

    return text


def clean_series(series):
    """Vectorized helper for cleaning a pandas Series of raw text."""
    return series.astype(str).apply(clean_text)
