# Student Score Predictor

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Visualization-4C72B0)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?logo=scikitlearn&logoColor=white)
![Linear Regression](https://img.shields.io/badge/Model-Linear%20Regression-success)
![Jupyter Notebook](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

A beginner-friendly Machine Learning project that predicts a student's exam score based on the number of study hours using **Simple Linear Regression**. This project demonstrates the complete workflow of loading data, cleaning it, training a model, making predictions, and evaluating performance.

---

## Project Overview

The goal of this project is to predict a student's score based on the number of hours they studied. It is an introductory regression project built using Python and Scikit-learn.

---

## Features

- Load and preprocess student score dataset
- Check for missing values
- Remove duplicate records
- Explore the dataset
- Train a Simple Linear Regression model
- Predict scores for custom study hours
- Evaluate model performance using regression metrics

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn

---

## Project Structure

```text
Student Score Predictor/
│
├── data/
│   └── score_updated.csv
│
├── Student_Score_Predictor.ipynb
├── README.md
└── requirements.txt
```

---

## Dataset

| Column | Description |
|---------|-------------|
| Hours | Number of hours studied |
| Scores | Student exam score |

---

## Machine Learning Workflow

1. Import required libraries
2. Load the dataset
3. Perform data cleaning
4. Explore the dataset
5. Train the Linear Regression model
6. Predict student scores
7. Evaluate the model

---

## Model

**Algorithm:** Linear Regression

**Input Feature**

- Hours

**Target Variable**

- Scores

---

## Evaluation Metrics

The model is evaluated using:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)

---

## Example

**Input**

```text
Study Hours: 7.5
```

**Output**

```text
Predicted Score: 75.6
```

> *Prediction value may vary depending on the dataset.*

---

## Installation

Clone the repository

```bash
git clone https://github.com/your-username/student-score-predictor.git
```

Move into the project directory

```bash
cd student-score-predictor
```

Install dependencies

```bash
pip install -r requirements.txt
```

Launch Jupyter Notebook

```bash
jupyter notebook
```

---

## Future Improvements

- Train-Test Split
- R² Score
- Model Serialization using Pickle
- Streamlit Web App
- Better Data Visualization

---

## Learning Outcomes

This project helped in understanding:

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Simple Linear Regression
- Model Training
- Prediction
- Regression Evaluation Metrics
- Basic Machine Learning Workflow

---

## Author

**Rohit Jha**

Aspiring AI Engineer | Machine Learning | Data Science

**LinkedIn:**  
https://www.linkedin.com/in/rohit-jha-ai/

---

## License

This project is licensed under the **MIT License**.