<b>This is only a learning project i am learning FASTAPI and tried to implement FASTAPI for practice 


## 🌐 Live Deployment

- **Live Application (Streamlit):** [Open Fake Job Posting Detector](https://fake-job-posting-detection-system-fastapi.streamlit.app/)
- **Backend API (Render):** [FastAPI Backend](https://fake-job-posting-detection-system.onrender.com)

# 🛡️ Fake Job Posting Detection System

A machine-learning web app that flags potentially fraudulent job advertisements **before** you apply or share personal details. Paste a single job ad to get an instant fraud-risk score, or upload a CSV to score hundreds of postings at once.

**Stack:** Python · scikit-learn · FastAPI · Streamlit · pandas

---

## ✨ Features

- **Single posting check** – enter a job title, description, company profile, etc. and get a verdict (*Genuine* / *Fraudulent*), a fraud probability and a risk gauge.
- **Bulk CSV upload** – upload a file of postings, see summary metrics (total, fraudulent, genuine, fraud rate), filter and sort the results, and download the full predictions as a CSV.
- **Red-flag checklist** – simple, explainable rule-based checks (scam wording, missing company profile, no salary, very short description, external links, …) shown next to the ML score.
- **REST API** – the model is served through FastAPI (`/predict`, `/fileupload`, `/health`) with auto-generated docs at `/docs`.
- **Demo samples** – one-click suspicious and genuine example postings in the sidebar.

---

## 🧠 How it works

```
Raw data → Cleaning → Text preparation + Feature engineering → Train/Test split
        → TF-IDF + Scaling → Model → Prediction → Evaluation
```

| Step | Details |
|------|---------|
| **Dataset** | EMSCAD fake job postings – 17,880 postings, 866 fraudulent (≈ 4.8 %) |
| **Text features** | `title + company_profile + description + requirements + benefits`, cleaned and vectorised with TF-IDF (10,000 features, unigrams + bigrams) |
| **Structured features (8)** | `telecommuting`, `has_company_logo`, `has_questions`, `has_salary`, `has_company_profile`, `has_requirements`, `has_benefits`, `text_length` |
| **Imbalance handling** | Stratified split + `class_weight` (balanced) |
| **Models compared** | Logistic Regression vs Random Forest (200 trees) – Random Forest chosen on fraud-class F1 |

### Model performance (20 % hold-out test set, 3,576 postings)

| Model | Accuracy | Precision (Fraud) | Recall (Fraud) | F1 (Fraud) | ROC-AUC |
|-------|---------:|------------------:|---------------:|-----------:|--------:|
| Logistic Regression | 0.9583 | 0.5426 | **0.8844** | 0.6725 | 0.9897 |
| **Random Forest** (deployed) | 0.9804 | **1.0000** | 0.5954 | **0.7464** | **0.9904** |

> Accuracy alone is misleading here – predicting "genuine" for everything already gives ~95 %. Precision, recall and F1 on the **fraud class** are the metrics that matter.

### Graphs

| Class distribution | ROC curve |
|:--:|:--:|
| ![Class distribution](Graphs%20Used/Class_Distribution.png) | ![ROC curve](Graphs%20Used/ROC_Curve.png) |
| **Confusion matrix** | **Top fraud features** |
| ![Confusion matrix](Graphs%20Used/Confusion_Matrix.png) | ![Top fraud features](Graphs%20Used/Top_Fraud_Features.png) |

More plots are in the [`Graphs Used`](Graphs%20Used) folder.

---

## 📁 Project structure

```
Fake Job Posting Detection System/
├── app.py                 # Streamlit frontend (single check + bulk CSV upload)
├── fastapi_app.py         # FastAPI backend (/predict, /fileupload, /health)
├── simple-streamlit.py    # Minimal Streamlit client (learning example)
├── requirements.txt
├── data/
│   └── fake_job_postings.csv
├── models/
│   ├── fake_job_model.pkl     # trained Random Forest
│   ├── tfidf_vectorizer.pkl
│   ├── scaler.pkl
│   └── num_cols.pkl           # numeric feature order used in training
├── notebook/
│   └── Fake Job Posting Detection System.ipynb   # EDA, training, evaluation
└── Graphs Used/               # plots exported from the notebook
```

---

## 🚀 Getting started

### 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the backend (terminal 1)

Run this from the project folder, because the models are loaded using relative paths.

```bash
uvicorn fastapi_app:app --reload
```

The API runs at `http://127.0.0.1:8000` (interactive docs at `http://127.0.0.1:8000/docs`).

### 3. Start the frontend (terminal 2)

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`). The sidebar shows whether the API is online. If your backend runs on another address, change it in the **FastAPI URL** field.

---

## 📂 Using the bulk CSV upload

Scroll down to **Upload a CSV of job postings** in the app, choose a `.csv` file and click **Analyse file**.

Your CSV must contain these columns (any extra columns are kept in the output):

| Column | Type | Notes |
|--------|------|-------|
| `title` | text | |
| `company_profile` | text | can be empty |
| `description` | text | |
| `requirements` | text | can be empty |
| `benefits` | text | can be empty |
| `salary_range` | text | can be empty |
| `telecommuting` | 0 / 1 | remote job |
| `has_company_logo` | 0 / 1 | |
| `has_questions` | 0 / 1 | screening questions |

Click **Download sample CSV template** in the app to get a ready-made example. The result adds three columns: `prediction`, `fraud_probability` and `fraud_percentage`.

> The original dataset (`data/fake_job_postings.csv`) already has all required columns, so you can upload it directly. Postings are scored one row at a time, so very large files (thousands of rows) take a while – try a few hundred rows first.

---

## 🔌 API reference

### `GET /health`

```json
{ "status": "API is running", "model_loaded": true, "vectorizer_loaded": true }
```

### `POST /predict`

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Work From Home Data Entry - Earn $5000 Weekly",
        "description": "No experience needed! Send your bank details and a registration fee to get started.",
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_questions": 0
      }'
```

Response:

```json
{
  "prediction": "Fraudulent Job Posting",
  "fraud_probability": 0.745,
  "fraud_percentage": 74.5,
  "status": "success"
}
```

`title` (min 3 chars) and `description` (min 10 chars) are required; all other fields are optional.

### `POST /fileupload`

Accepts a CSV (`multipart/form-data`, field name `file`) and returns it as a CSV with the prediction columns added.

```bash
curl -X POST http://127.0.0.1:8000/fileupload \
  -F "file=@job_postings.csv" \
  -o job_predictions.csv
```

Returns `400` if the file is not a `.csv` or required columns are missing.

---

## ⚠️ Limitations

- The deployed Random Forest has **perfect precision but only ~60 % recall** on fraud – it rarely raises a false alarm, but it misses some scams. A fraud-free result is **not** a guarantee that a job is real.
- The model is trained on one public dataset (EMSCAD) and may not capture newer scam patterns.
- The red-flag checklist is rule-based and independent from the ML score.

**Always verify the employer independently** (official website, LinkedIn, reviews) and never pay money to get a job.

---

## 🗺️ Possible improvements

- Lower the decision threshold or use `class_weight` tuning to improve fraud recall
- Add model explainability (e.g. top contributing words per prediction)
- Vectorise bulk scoring so large CSVs run faster
- Deploy the API and UI (Render / Streamlit Community Cloud)

---

## 👤 Author

**Rohit Jha** · [GitHub](https://github.com/Rohit-coder-py) · [LinkedIn](https://linkedin.com/in/rohit-jha-ai)
