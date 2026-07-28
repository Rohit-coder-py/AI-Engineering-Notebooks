"""
Turns a single raw customer record (the kind of values a person picks in the
Streamlit form) into the exact 30-column encoded row the model expects -
same encoding the notebook uses: LabelEncoder-style binary mapping for the
yes/no columns, one-hot (drop_first) for the multi-category columns.
"""

import pandas as pd

# same binary columns the notebook label-encodes (alphabetical LabelEncoder
# behaviour: No/Female -> 0, Yes/Male -> 1)
BINARY_MAP = {
    "gender": {"Female": 0, "Male": 1},
    "Partner": {"No": 0, "Yes": 1},
    "Dependents": {"No": 0, "Yes": 1},
    "PhoneService": {"No": 0, "Yes": 1},
    "PaperlessBilling": {"No": 0, "Yes": 1},
}

MULTI_COLS = [
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaymentMethod",
]


def build_feature_row(raw: dict, feature_order: list) -> pd.DataFrame:
    """
    raw: dict of raw form values, e.g.
        {
            "gender": "Female", "SeniorCitizen": 0, "Partner": "Yes",
            "Dependents": "No", "tenure": 12, "PhoneService": "Yes",
            "MultipleLines": "No", "InternetService": "Fiber optic",
            "OnlineSecurity": "No", "OnlineBackup": "Yes",
            "DeviceProtection": "No", "TechSupport": "No",
            "StreamingTV": "Yes", "StreamingMovies": "No",
            "Contract": "Month-to-month", "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",
            "MonthlyCharges": 70, "TotalCharges": 840.5,
        }
    feature_order: exact column order the scaler/model were fit on
                   (models/feature_order.pkl)
    Returns a single-row DataFrame with columns == feature_order.
    """
    row = {}

    # binary yes/no style columns
    for col, mapping in BINARY_MAP.items():
        row[col] = mapping[raw[col]]

    row["SeniorCitizen"] = int(raw["SeniorCitizen"])
    row["tenure"] = float(raw["tenure"])
    row["MonthlyCharges"] = float(raw["MonthlyCharges"])
    row["TotalCharges"] = float(raw["TotalCharges"])

    # start every one-hot column at 0, then flip on the one that matches
    one_hot_cols = [c for c in feature_order if c not in row]
    for c in one_hot_cols:
        row[c] = 0

    for col in MULTI_COLS:
        value = raw[col]
        dummy_name = f"{col}_{value}"
        if dummy_name in row:
            row[dummy_name] = 1
        # if it's the dropped baseline category, every dummy for that
        # column just stays 0 - exactly like pd.get_dummies(drop_first=True)

    df_row = pd.DataFrame([row])
    return df_row[feature_order]
