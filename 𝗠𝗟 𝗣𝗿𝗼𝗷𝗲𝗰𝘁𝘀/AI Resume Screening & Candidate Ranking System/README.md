# AI TalentScout

## Intelligent Resume Screening & Candidate Ranking System

------------------------------------------------------------------------

# Project Status

**Status : Completed**

## Important Note

This project successfully demonstrates the complete end-to-end Machine
Learning workflow, including data preprocessing, exploratory data
analysis (EDA), feature engineering, encoding, feature scaling, model
training, and model evaluation.

During experimentation, multiple classification algorithms produced
nearly identical performance. Further investigation showed that the
dataset contains **very weak relationships between the input features
and the target variable**, causing most models to predict the majority
class.

As a result, the primary limitation lies in the **dataset rather than
the machine learning implementation**. This project demonstrates an
important real-world machine learning lesson: **high-quality data is
often more important than choosing a different algorithm.**

------------------------------------------------------------------------

# Limitations

➜ Very weak correlation between input features and the target variable.

➜ Multiple classification algorithms achieved nearly identical
performance.

➜ The dataset contains limited predictive information.

➜ Most models predominantly predicted the majority class.

➜ Further hyperparameter tuning is unlikely to produce significant
improvements without a better dataset.

------------------------------------------------------------------------

# What I Learned

➜ Performed complete Exploratory Data Analysis (EDA).

➜ Checked missing values, duplicate records and outliers.

➜ Applied Label Encoding to categorical features.

➜ Applied StandardScaler for feature scaling.

➜ Performed Train-Test Split.

➜ Trained multiple Machine Learning classification models.

➜ Evaluated models using Accuracy, Precision, Recall and F1 Score.

➜ Compared different Machine Learning algorithms.

➜ Investigated prediction behaviour instead of relying only on accuracy.

➜ Analyzed feature-target correlations.

➜ Learned how to identify whether poor model performance is caused by
the dataset or the algorithm.

➜ Understood the importance of data quality in Machine Learning.

------------------------------------------------------------------------

# Project Structure

``` text
AI TalentScout
│
├── dataset
│   ├── resume_dataset_200k_enhanced.csv
│   └── resume_dataset_encoded.csv
│
├── graphs
│   ├── age_Distribution.png
│   ├── certifications_Distribution.png
│   ├── cgpa_Distribution.png
│   ├── experience_years_Distribution.png
│   ├── hackathons_Distribution.png
│   ├── hired_Distribution.png
│   ├── Hiring Distribution.png
│   ├── internships_Distribution.png
│   ├── programming_languages_Distribution.png
│   ├── projects_Distribution.png
│   ├── research_papers_Distribution.png
│   ├── resume_length_words_Distribution.png
│   ├── skills_score_Distribution.png
│   └── soft_skills_score_Distribution.png
│
└── notebooks
    └── AI TalentScout.ipynb
```

------------------------------------------------------------------------

# Dataset

Approximately **200,000 candidate records**.

### Features

➜ Age

➜ Education Level

➜ University Tier

➜ CGPA

➜ Internships

➜ Projects

➜ Programming Languages

➜ Certifications

➜ Experience Years

➜ Hackathons

➜ Research Papers

➜ Skills Score

➜ Soft Skills Score

➜ Resume Length (Words)

➜ Company Type

### Target Variable

➜ 0 → Not Hired

➜ 1 → Hired

------------------------------------------------------------------------

# Exploratory Data Analysis

The project includes:

➜ Dataset Understanding

➜ Missing Value Analysis

➜ Duplicate Value Analysis

➜ Outlier Detection

➜ Hiring Distribution

➜ Feature Distribution Analysis

➜ Observations for every feature

------------------------------------------------------------------------

# Data Preprocessing

➜ Removed Candidate ID

➜ Label Encoding

➜ Train-Test Split

➜ Feature Scaling using StandardScaler

------------------------------------------------------------------------

# Machine Learning Models

➜ Logistic Regression

➜ Gaussian Naive Bayes

➜ Random Forest Classifier

------------------------------------------------------------------------

# Evaluation Metrics

➜ Accuracy Score

➜ Precision Score

➜ Recall Score

➜ F1 Score

------------------------------------------------------------------------

# Project Findings

➜ Multiple Machine Learning models were trained and evaluated.

➜ All models achieved similar performance.

➜ Feature-target correlation analysis showed extremely weak
relationships.

➜ Dataset quality limited predictive performance.

➜ The primary limitation was the dataset rather than the Machine
Learning algorithms.

------------------------------------------------------------------------

# Technologies Used

➜ Python

➜ Pandas

➜ NumPy

➜ Matplotlib

➜ Seaborn

➜ Scikit-learn

➜ Jupyter Notebook

------------------------------------------------------------------------

# Author

**Rohit Jha**

GitHub: https://github.com/Rohit-coder-py
