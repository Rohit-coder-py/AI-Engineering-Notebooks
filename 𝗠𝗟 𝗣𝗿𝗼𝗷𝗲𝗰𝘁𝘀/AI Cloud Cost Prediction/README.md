# ☁️ AI Cloud Cost Predictor

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?logo=scikitlearn)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?logo=numpy)
![License](https://img.shields.io/badge/License-MIT-green)

> **Predict Azure cloud billing costs using Machine Learning.**

---

## 📖 Overview

Modern cloud platforms like **Microsoft Azure** generate thousands of billing records every day. As organizations deploy Virtual Machines, Storage, Databases, Networking, and AI services, understanding future cloud costs becomes increasingly challenging.

Unexpected cloud expenses can lead to **budget overruns, inefficient resource allocation, and reduced cost visibility**.

**AI Cloud Cost Predictor** addresses this problem by estimating the billing cost of an Azure resource **before the invoice is generated**. Using historical Azure billing data and Machine Learning, the application predicts the expected **CostInBillingCurrency** from service information, resource location, meter details, and billing date.

The project demonstrates a complete end-to-end Machine Learning workflow, from data analysis and feature engineering to model deployment using Streamlit.

---

## 🚀 Live Demo

**🌐 Streamlit Application**

https://ai-cloud-cost-predictor.streamlit.app/

---

## 📸 Application Preview

| Home Page                                         | Input Interface                                   |
| ------------------------------------------------- | ------------------------------------------------- |
| ![](preview/Screenshot%202026-07-07%20201930.png) | ![](preview/Screenshot%202026-07-07%20201936.png) |

### Prediction Result

<p align="center">
<img src="preview/Screenshot%202026-07-07%20202029.png" width="900">
</p>

---

## ✨ Features

* 📊 Exploratory Data Analysis (EDA)
* 🧹 Data Cleaning & Feature Engineering
* 📅 Date Feature Extraction
* 🔄 Manual Feature Encoding (No Pipeline)
* 🤖 Linear Regression Model
* 📈 Model Performance Evaluation
* 🌐 Interactive Streamlit Web Application
* 💾 Saved Model & Preprocessing Artifacts

---

## 🛠️ Tech Stack

| Category             | Technologies        |
| -------------------- | ------------------- |
| Programming Language | Python              |
| Data Analysis        | Pandas, NumPy       |
| Data Visualization   | Matplotlib, Seaborn |
| Machine Learning     | Scikit-learn        |
| Web Application      | Streamlit           |
| Model Serialization  | Pickle              |

---

## 📂 Project Structure

```text
AI-Cloud-Cost-Predictor
│
├── app.py
├── README.md
├── requirements.txt
│
├── data/
│   └── anonymized_costs.csv
│
├── images/
│   ├── EDA Visualizations
│
├── models/
│   ├── linear_regression_model.pkl
│   ├── scaler.pkl
│   ├── onehot_encoder.pkl
│   ├── ordinal_encoder.pkl
│   ├── feature_schema.pkl
│   └── category_options.pkl
│
├── notebooks/
│   └── Cloud_Cost_Predictior.ipynb
│
└── preview/
    ├── Home Page
    ├── Input Interface
    └── Prediction Result
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/rohitjha7386/AI-Cloud-Cost-Predictor.git
```

Move into the project directory

```bash
cd AI-Cloud-Cost-Predictor
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Streamlit application

```bash
streamlit run app.py
```

---

## 📊 Machine Learning Workflow

```text
Azure Billing Data
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Feature Encoding
        │
        ▼
Linear Regression
        │
        ▼
Model Evaluation
        │
        ▼
Streamlit Deployment
```

---

## 👨‍💻 Author

**Rohit Jha**

**Aspiring AI Engineer | Building Real-World AI & Machine Learning Projects**

* **GitHub:** https://github.com/rohitjha7386
* **LinkedIn:** https://linkedin.com/in/rohit-jha-ai

---

⭐ **If you found this project useful, consider giving it a star!**
