# Employee Attrition Prediction & HR Analytics System

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end Machine Learning project that predicts whether an employee is likely to leave an organization using HR analytics data. The project covers data preprocessing, model comparison, hyperparameter tuning, and deployment with Streamlit.

---

## Live Demo

**Application:**
https://employee-attrition-predictor-harsh.streamlit.app/

---

## Application Preview

> Screenshots will be added soon.

---

## Project Overview

This project uses Machine Learning to predict employee attrition based on employee demographics, job-related information, and workplace satisfaction. Multiple classification algorithms were trained, evaluated, and compared before selecting the final model for deployment.

---

## Features

* Data Cleaning & Preprocessing
* Label Encoding & One-Hot Encoding
* Feature Scaling using StandardScaler
* Multiple Classification Models
* Model Comparison
* Hyperparameter Tuning (GridSearchCV & RandomizedSearchCV)
* Streamlit Web Application
* Model Serialization using Pickle

---

## Models Used

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

## Final Model

**Support Vector Machine (SVM)**

```python
C = 0.1
kernel = "linear"
gamma = "scale"
```

---

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Streamlit
* Matplotlib
* Seaborn

---

## Project Structure

```text
Employee-Attrition-Prediction-ML-Model/
│
├── Final App/
├── data/
├── models/
├── Notebook/
├── screenshots/
├── README.md
└── requirements.txt
```

---

## Author

**Rohit Jha**

Aspiring AI & Machine Learning Engineer

---

If you found this project useful, consider giving it a ⭐ on GitHub.
