import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET_COLUMN = "annual_medical_cost"

# columns dropped because they are identifiers or they leak target information
UNWANTED_COLUMNS = [
    "person_id",
    "annual_premium",
    "monthly_premium",
    "claims_count",
    "avg_claim_amount",
    "total_claims_paid",
    "risk_score",
    "is_high_risk",
    "had_major_procedure",
    "alcohol_freq",  # ~30% missing values, dropping instead of imputing
]


def load_data(path):
    return pd.read_csv(path)


def clean_data(df):
    columns_to_drop = [c for c in UNWANTED_COLUMNS if c in df.columns]
    return df.drop(columns=columns_to_drop)


def get_feature_types(X):
    categorical_columns = X.select_dtypes(include="object").columns.tolist()
    numerical_columns = X.select_dtypes(include=["number"]).columns.tolist()
    return categorical_columns, numerical_columns


def fit_transform(X_train, X_valid, X_test, categorical_columns, numerical_columns):
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    X_train_cat = encoder.fit_transform(X_train[categorical_columns])
    X_valid_cat = encoder.transform(X_valid[categorical_columns])
    X_test_cat = encoder.transform(X_test[categorical_columns])

    scaler = StandardScaler()
    X_train_num = scaler.fit_transform(X_train[numerical_columns])
    X_valid_num = scaler.transform(X_valid[numerical_columns])
    X_test_num = scaler.transform(X_test[numerical_columns])

    X_train_final = np.hstack([X_train_num, X_train_cat])
    X_valid_final = np.hstack([X_valid_num, X_valid_cat])
    X_test_final = np.hstack([X_test_num, X_test_cat])

    encoded_cat_names = encoder.get_feature_names_out(categorical_columns).tolist()
    feature_order = numerical_columns + encoded_cat_names

    return X_train_final, X_valid_final, X_test_final, encoder, scaler, feature_order


def transform_single(raw_input, encoder, scaler, categorical_columns, numerical_columns):
    df = pd.DataFrame([raw_input])
    num_part = scaler.transform(df[numerical_columns])
    cat_part = encoder.transform(df[categorical_columns])
    return np.hstack([num_part, cat_part])


def save_artifacts(encoder, scaler, feature_meta, artifacts_dir):
    with open(os.path.join(artifacts_dir, "encoder.pkl"), "wb") as f:
        pickle.dump(encoder, f)

    with open(os.path.join(artifacts_dir, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)

    with open(os.path.join(artifacts_dir, "feature_order.pkl"), "wb") as f:
        pickle.dump(feature_meta, f)


def load_artifacts(artifacts_dir):
    with open(os.path.join(artifacts_dir, "encoder.pkl"), "rb") as f:
        encoder = pickle.load(f)

    with open(os.path.join(artifacts_dir, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)

    with open(os.path.join(artifacts_dir, "feature_order.pkl"), "rb") as f:
        feature_meta = pickle.load(f)

    return encoder, scaler, feature_meta
