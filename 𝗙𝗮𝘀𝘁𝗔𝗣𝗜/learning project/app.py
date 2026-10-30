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


#input schema

# Input Schema

class InputSchema(BaseModel):
    title: str = Field(..., min_length=3, description="Job title")

    company_profile: str = Field(default="", description="Company profile")
    description: str = Field(..., min_length=10, description="Job description")

    requirements: str = Field(default="", description="Job requirements")

    benefits: str = Field(default="", description="Job benefits")

    telecommuting: int = Field(default=0, ge=0, le=1)
    has_company_logo: int = Field(default=0, ge=0, le=1)
    has_questions: int = Field(default=0, ge=0, le=1)
    salary_range: str = Field(default="", description="Salary range")
    
    
    
#now creating routers
  
@app.get("/")
def home():
    return "Welcome to Fake Job Posting Detection System"
    
