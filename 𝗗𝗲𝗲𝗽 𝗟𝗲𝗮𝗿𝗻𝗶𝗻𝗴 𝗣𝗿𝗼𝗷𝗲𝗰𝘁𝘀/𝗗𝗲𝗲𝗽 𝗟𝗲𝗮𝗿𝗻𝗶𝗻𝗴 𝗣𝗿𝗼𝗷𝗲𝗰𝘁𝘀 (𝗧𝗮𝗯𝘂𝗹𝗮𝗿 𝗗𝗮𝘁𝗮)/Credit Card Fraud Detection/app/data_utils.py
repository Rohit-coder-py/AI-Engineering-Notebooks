"""
Data + model loading utilities for the Streamlit app.
Everything here is cached so the app stays snappy after first load.
"""

import json
import os
import sys

import pandas as pd
import streamlit as st

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_DIR)
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "images")
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

sys.path.append(SRC_DIR)


@st.cache_resource(show_spinner=False)
def load_predictor():
    from infer import FraudPredictor
    return FraudPredictor(MODELS_DIR)


@st.cache_data(show_spinner=False)
def load_metrics():
    with open(os.path.join(MODELS_DIR, "metrics.json")) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_city_lookup():
    df = pd.read_json(os.path.join(MODELS_DIR, "city_lookup.json"))
    return df.set_index("city").to_dict(orient="index")


@st.cache_data(show_spinner=False)
def load_merchant_lookup():
    df = pd.read_json(os.path.join(MODELS_DIR, "merchant_lookup.json"))
    return df.set_index("merchant").to_dict(orient="index")


@st.cache_data(show_spinner=False)
def load_job_list():
    with open(os.path.join(MODELS_DIR, "job_list.json")) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_categories():
    return sorted([
        "entertainment", "food_dining", "gas_transport", "grocery_net",
        "grocery_pos", "health_fitness", "home", "kids_pets", "misc_net",
        "misc_pos", "personal_care", "shopping_net", "shopping_pos", "travel",
    ])


@st.cache_data(show_spinner=False)
def load_sample_transactions():
    return pd.read_csv(os.path.join(MODELS_DIR, "sample_transactions.csv"))


@st.cache_data(show_spinner=False)
def load_full_data(n_rows: int = 50000):
    """A capped sample of the full cleaned dataset, for analytics-page charts."""
    return pd.read_csv(os.path.join(DATA_DIR, "credit_card_frauds_cleaned.csv"), nrows=n_rows)


def image_path(name: str) -> str:
    return os.path.join(IMAGES_DIR, name)
