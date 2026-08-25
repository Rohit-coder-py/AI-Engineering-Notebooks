#file use :

"""
Take the raw values coming from your future Streamlit UI
and perform the same encoding + scaling that was used when the final model was trained
"""

# User enters/selects values
#           ↓
#    preprocessing.py
#           ↓
# Categorical encoding
#           ↓
# Feature ordering
#           ↓
# Numerical scaling
#           ↓
# PyTorch tensor
#           ↓
#        Model




#start from here



# ---------------------------------------------------------
# preprocessing.py
#
# COPIED FROM (and adapted from) TWO PLACES in the notebook:
#   1. The "#encoding categorical column" cell -> OrdinalEncoder step
#  2. The "#scaling" cell -> StandardScaler step
# ------------------------------------------------------------
# 
import joblib
import pandas as pd

"""
    Loads everything that was joblib.dump()'d at the end of the
    notebook (the "Save everything needed for deployment" cell).
    Returns them as a dict so the rest of the app can just ask
    for artifacts["scaler"], artifacts["encoder"], etc.
"""


def load_artifacts(models_dir="models"):
    artifacts = {
        "scaler": joblib.load(f"{models_dir}/scaler.pkl"),
        "encoder": joblib.load(f"{models_dir}/encoder.pkl"),
        "feature_order": joblib.load(f"{models_dir}/feature_order.pkl"),
        "categorical_columns": joblib.load(f"{models_dir}/categorical_columns.pkl"),
        "numerical_columns": joblib.load(f"{models_dir}/numerical_columns.pkl"),
        "best_hyperparameters": joblib.load(f"{models_dir}/best_hyperparameters.pkl"),
    }
    return artifacts

# ========================================================

"""
    Takes the raw values a user picked in the Streamlit form
    (as a plain dict) and turns them into a scaled numpy array
    the model can accept -- same shape/order as X_train had.

    Steps (identical order to the notebook):
      1. Put values into a DataFrame, one row, columns in feature_order.
      2. Encode categorical columns with the ALREADY-FITTED encoder.
      3. Scale ALL columns with the ALREADY-FITTED scaler.
"""











def preprocess_input(input_dict, artifacts):
    feature_order = artifacts["feature_order"]
    categorical_columns = artifacts["categorical_columns"]
    encoder = artifacts["encoder"]
    scaler = artifacts["scaler"]

    # Step 1: one-row dataframe, correct column order
    df = pd.DataFrame([input_dict])
    df = df[feature_order]

    # Step 2: encode categorical columns (encoder.transform, NOT fit_transform --
    # fitting only happens during training, inference only ever transforms)
    df[categorical_columns] = encoder.transform(df[categorical_columns])

    # Step 3: scale the full row (scaler was fit on the full feature set,
    # after encoding, not just the numerical columns)
    scaled_array = scaler.transform(df)

    return scaled_array














"""
basically preprocessing.py means :

load_artifacts()
      │
      └── Gets the tools we saved during training


preprocess_input()
      │
      └── Uses those tools on NEW user input
      
      
"""
