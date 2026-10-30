#this is a a sample streamlit file and simplest frontend for the  project (not the main file)

#as i already creating fastapi routes the goal of this file is to learn how we connect streamlit with our fastapi 
#server and access data from there  


# Simplest Streamlit app that talks to our FastAPI
#
# Step 1 (terminal 1):  uvicorn app:app --reload
# Step 2 (terminal 2):  streamlit run simple_streamlit.py

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"   # FastAPI /predict route

st.title("Fake Job Posting Detector")

#inputs
title = st.text_input("Job Title")
description = st.text_area("Job Description")
company_profile = st.text_area("Company Profile (optional)")
requirements = st.text_area("Requirements (optional)")
benefits = st.text_area("Benefits (optional)")
salary_range = st.text_input("Salary Range (optional)")

telecommuting = st.checkbox("Remote job?")
has_company_logo = st.checkbox("Has company logo?")
has_questions = st.checkbox("Has screening questions?")

if st.button("Check"):
    data = {
        "title": title,
        "description": description,
        "company_profile": company_profile,
        "requirements": requirements,
        "benefits": benefits,
        "salary_range": salary_range,
        "telecommuting": int(telecommuting),
        "has_company_logo": int(has_company_logo),
        "has_questions": int(has_questions),
    }

    response = requests.post(API_URL, json=data)   #main connection

    if response.status_code == 200:
        result = response.json()
        st.write(result)
        st.write("\n\n\n ====================================")
        st.write("Prediction:", result["prediction"])
        st.write("Fraud Probability:", result["fraud_percentage"], "%")
    else:
        st.error("Error: " + response.text)