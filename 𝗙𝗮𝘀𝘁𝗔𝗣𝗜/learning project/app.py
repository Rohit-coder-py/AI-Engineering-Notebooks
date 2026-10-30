import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI,HTTPException

from pydantic import BaseModel,Field

app = FastAPI()

model = joblib.load("models/fake_job_model.pkl")
tfidf = joblib.load("models/tfidf_vectorizer.pkl")
num_cols = joblib.load("models/num_cols.pkl")
scaler = joblib.load("models/scaler.pkl")


print(model)
