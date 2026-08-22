

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib


DROP_COLS = ["transaction_id", "user_id", "addiction_level"]
TARGET_COL = "addicted_label"

CATEGORICAL_COLS = ["gender", "stress_level", "academic_work_impact"]
NUMERICAL_COLS = [
    "age",
    "daily_screen_time_hours",
    "social_media_hours",
    "gaming_hours",
    "work_study_hours",
    "sleep_hours",
    "notifications_per_day",
    "app_opens_per_day",
    "weekend_screen_time",
]


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Force plain numpy dtypes (pandas' newer nullable/string backends can
    # otherwise silently fall back to object dtype once mixed with one-hot
    # columns downstream, which breaks torch.tensor conversion).
    for col in df.columns:
        if pd.api.types.is_integer_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            df[col] = df[col].astype("float64" if pd.api.types.is_float_dtype(df[col]) else "int64")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drops identifier columns and `addiction_level`, which is a direct
    leakage column (it is a categorical restatement of the target:
    Mild -> 0, Moderate/Severe -> 1, and is otherwise NaN). Keeping it
    would let the model "cheat" instead of learning from behaviour.
    """
    df = df.copy()
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])
    df = df.drop_duplicates()
    return df


def encode_categoricals(df: pd.DataFrame, encoders: dict | None = None):
    """
    One-hot encodes categorical columns. If `encoders` (a dict of
    {col: sorted unique categories}) is provided, reindexes to match
    those exact dummy columns (needed at inference time so the input
    shape always matches what the model was trained on).
    """
    df = df.copy()
    fitted_encoders = {}

    for col in CATEGORICAL_COLS:
        dummies = pd.get_dummies(df[col], prefix=col, dtype="int64")
        if encoders is not None:
            expected_cols = encoders[col]
            for c in expected_cols:
                if c not in dummies.columns:
                    dummies[c] = 0
            dummies = dummies[expected_cols]
        else:
            fitted_encoders[col] = list(dummies.columns)
        df = pd.concat([df.drop(columns=[col]), dummies], axis=1)

    if encoders is None:
        return df, fitted_encoders
    return df


def get_feature_target(df: pd.DataFrame):
    y = df[TARGET_COL].values.astype(np.float32)
    X = df.drop(columns=[TARGET_COL])
    return X, y


def fit_scaler(X: pd.DataFrame) -> StandardScaler:
    scaler = StandardScaler()
    scaler.fit(X[NUMERICAL_COLS])
    return scaler


def apply_scaler(X: pd.DataFrame, scaler: StandardScaler) -> pd.DataFrame:
    X = X.copy()
    X[NUMERICAL_COLS] = scaler.transform(X[NUMERICAL_COLS])
    return X


def save_artifacts(scaler, encoders, feature_order, out_dir: str):
    joblib.dump(scaler, f"{out_dir}/scaler.pkl")
    joblib.dump(encoders, f"{out_dir}/encoders.pkl")
    joblib.dump(feature_order, f"{out_dir}/feature_order.pkl")


def load_artifacts(out_dir: str):
    scaler = joblib.load(f"{out_dir}/scaler.pkl")
    encoders = joblib.load(f"{out_dir}/encoders.pkl")
    feature_order = joblib.load(f"{out_dir}/feature_order.pkl")
    return scaler, encoders, feature_order
