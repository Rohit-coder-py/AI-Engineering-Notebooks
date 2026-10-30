#wrap the project into fastapi

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


#text Cleaning Function

import re
from scipy.sparse import hstack, csr_matrix


def clean_text(text):

    text = str(text).lower()

    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'http\S+|www\.\S+', ' url ', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text



@app.post("/predict")
def predict(data: InputSchema):

    try:

        
        title = data.title
        company_profile = data.company_profile
        description = data.description
        requirements = data.requirements
        benefits = data.benefits
        
        text = clean_text(
            ' '.join([
                title,
                company_profile,
                description,
                requirements,
                benefits
            ])
        )

        #create numerical features
        user_data = pd.DataFrame([{

            'telecommuting': data.telecommuting,

            'has_company_logo': data.has_company_logo,

            'has_questions': data.has_questions,

            'has_salary': int(data.salary_range.strip() != ''),

            'has_company_profile': int(
                company_profile.strip() != ''
            ),

            'has_requirements': int(
                requirements.strip() != ''
            ),

            'has_benefits': int(
                benefits.strip() != ''
            ),

            'text_length': len(text.split())

        }])

        #Maintain training feature order
        user_data = user_data[num_cols]

        # TF-IDF transformation
        text_features = tfidf.transform([text])

        #Scale numerical features
        numerical_features = scaler.transform(user_data)

        # 6. Combine both feature matrices
        final_features = hstack([
            text_features,
            csr_matrix(numerical_features)
        ]).tocsr()

        # 7. Make prediction
        prediction = model.predict(final_features)[0]

        # 8. Calculate probability
        probability = model.predict_proba(final_features)[0][1]

        # 9. Prepare response
        result = (
            "Fraudulent Job Posting"
            if prediction == 1
            else "Genuine Job Posting"
        )

        return {

            "prediction": result,

            "fraud_probability": round(
                float(probability), 4
            ),

            "fraud_percentage": round(
                float(probability * 100), 2
            ),

            "status": "success"

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



#Health Check Route


@app.get("/health")
def health_check():

    return {
        "status": "API is running",
        "model_loaded": model is not None,
        "vectorizer_loaded": tfidf is not None
    }


#Adding file upload feature in app 



    
