"""
Preprocessing helpers for Credit Card Fraud Detection.

Reproduces the exact cleaning / encoding / scaling pipeline from
`notebooks/Credit Card Fraud Detection.ipynb`:

1. Drop `trans_date_trans_time`, `dob`, `trans_num` (raw data only —
   the shipped `data/credit_card_frauds_cleaned.csv` already has this done).
2. Split features into categorical / numerical.
3. `OrdinalEncoder` on categorical columns (fit on train, unknown -> -1).
4. `StandardScaler` on the full feature set (fit on train).

Column order used everywhere:
    ['merchant', 'category', 'amt', 'city', 'state',
     'lat', 'long', 'city_pop', 'job', 'merch_lat', 'merch_long']
"""

import joblib
import pandas as pd

RAW_DROP_COLUMNS = ["trans_date_trans_time", "dob", "trans_num"]


def clean_raw(df: pd.DataFrame) -> pd.DataFrame:
    """Drop identifier / leakage columns from a raw dataframe."""
    cols_to_drop = [c for c in RAW_DROP_COLUMNS if c in df.columns]
    return df.drop(columns=cols_to_drop)


class FraudPreprocessor:
    """Wraps the fitted encoder + scaler + column order for inference."""

    def __init__(self, models_dir: str):
        self.encoder = joblib.load(f"{models_dir}/encoder.pkl")
        self.scaler = joblib.load(f"{models_dir}/scaler.pkl")
        self.categorical_columns = joblib.load(f"{models_dir}/categorical_columns.pkl")
        self.numerical_columns = joblib.load(f"{models_dir}/numerical_columns.pkl")
        self.feature_order = joblib.load(f"{models_dir}/feature_order.pkl")

    def transform(self, df: pd.DataFrame):
        """
        Take a raw-feature dataframe (columns matching `feature_order`,
        any order) and return a scaled numpy array ready for the model.
        """
        X = df[self.feature_order].copy()
        X[self.categorical_columns] = self.encoder.transform(X[self.categorical_columns])
        X_scaled = self.scaler.transform(X)
        return X_scaled
