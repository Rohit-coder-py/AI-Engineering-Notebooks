# Employee Attrition Prediction & HR Analytics System

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end Machine Learning project that predicts whether an employee is likely to leave an organization using HR analytics data. This project covers the complete machine learning workflow including data preprocessing, exploratory data analysis, feature engineering, model training, model comparison, hyperparameter tuning, and deployment using Streamlit.

---

# Live Demo

**Application**

https://employee-attrition-predictor-harsh.streamlit.app/

---

# Application Preview

> Screenshots will be added soon.

---

# Project Overview

Employee attrition is one of the biggest challenges faced by organizations. Predicting employee turnover allows HR departments to identify employees who are at risk of leaving and take proactive measures to improve employee retention.

This project uses HR analytics data to build and compare multiple classification models. After evaluating different algorithms and performing hyperparameter tuning, the best-performing model was selected and deployed as a Streamlit web application.

---

# Features

* Complete End-to-End Machine Learning Pipeline
* Data Cleaning & Preprocessing
* Exploratory Data Analysis (EDA)
* Feature Engineering
* Label Encoding & One-Hot Encoding
* Feature Scaling using StandardScaler
* Multiple Machine Learning Models
* Cross Validation
* Hyperparameter Tuning using GridSearchCV & RandomizedSearchCV
* Model Comparison
* Model Serialization using Pickle
* Interactive Streamlit Web Application


---

# Models Used

* Logistic Regression
* K-Nearest Neighbors (KNN)
* Support Vector Machine (SVM)
* Gaussian Naive Bayes
* Decision Tree
* Random Forest
* AdaBoost
* Gradient Boosting
* XGBoost
* Stacking Classifier

---

# Final Model

**Support Vector Machine (SVM)**

```python
C = 0.1
kernel = "linear"
gamma = "scale"
```

---

# Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Streamlit
* Matplotlib
* Seaborn

---

# Project Structure

```text
C:.
│   README.md
│   requirements.txt
│
├───𝗗𝗮𝘁𝗮 𝗔𝗻𝗮𝗹𝘆𝘀𝗶𝘀 𝗮𝗻𝗱 𝗩𝗶𝘀𝘂𝗮𝗹𝗶𝘇𝗮𝘁𝗶𝗼𝗻
│       Categorical Plots.ipynb
│       Distributution Plots.ipynb
│       Matplotlib.ipynb
│       Matrix Plot.ipynb
│       Numpy.ipynb
│       Pandas.ipynb
│       Plottly and Cufflin .ipynb
│       Regression Plots.ipynb
│
├───𝗠𝗟 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀
│   │   Student Score Prediction Project.ipynb
│   │
│   ├───Employee Attrition Prediction & HR Analytics System
│   │   │   README.md
│   │   │   requirements.txt
│   │   │
│   │   ├───data
│   │   │       cleaned_employee_attrition.csv
│   │   │       encoded_employee_attrition.csv
│   │   │       WA_Fn-UseC_-HR-Employee-Attrition.csv
│   │   │
│   │   ├───Final App
│   │   │       app.py
│   │   │
│   │   ├───models
│   │   │       employee_attrition_scaler.pkl
│   │   │       employee_attrition_svm.pkl
│   │   │
│   │   ├───Notebook
│   │   │       Employee Attrition Prediction & HR Analytics System.ipynb
│   │   │
│   │   └───screenshots
│   │
│   ├───Employee Salary Predictor
│   ├───Heart Disease Predictor
│   ├───Loan Approval Predictor
│   └───Students Success Predictor Model
│
├───𝗠𝗮𝗰𝗵𝗶𝗻𝗲 𝗟𝗲𝗮𝗿𝗻𝗶𝗻𝗴
│       Machine Learning.ipynb
│
└───𝗠𝗮𝘁𝗵𝗲𝗺𝗮𝘁𝗶𝗰𝘀
        Mathemetics.ipynb

# Author

** Rohit Jha **

Aspiring Artificial Intelligence Engineer

If you found this project useful, consider giving it a ⭐ on GitHub.
