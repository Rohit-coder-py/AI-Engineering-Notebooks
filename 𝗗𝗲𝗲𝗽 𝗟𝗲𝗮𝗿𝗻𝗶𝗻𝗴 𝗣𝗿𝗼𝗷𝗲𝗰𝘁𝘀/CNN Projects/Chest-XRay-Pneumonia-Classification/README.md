<div align="center">

# 🩻 Chest X-Ray Pneumonia Classification

### AI-powered chest radiograph analysis using a custom PyTorch CNN

*Classifies chest X-rays as **NORMAL** or **PNEUMONIA**, with a live confidence breakdown — served through a Streamlit web app.*

**[🚀 Live Demo](https://chest-x-ray-pneumonial-predictor-pytorch.streamlit.app/)**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chest-x-ray-pneumonial-predictor-pytorch.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1%2B-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![torchvision](https://img.shields.io/badge/torchvision-0.16%2B-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-Educational-lightgrey?style=flat-square)

</div>

<br>

## 📖 Overview

**Chest X-Ray Pneumonia Classification** is an end-to-end deep learning project that trains a **custom convolutional neural network from scratch** — no pretrained backbone — to distinguish healthy chest radiographs from those showing signs of pneumonia. The trained model is wrapped in a clean, tab-based **Streamlit** interface where anyone can upload a chest X-ray and instantly get a prediction with a full class-probability breakdown.

The project intentionally covers the *entire* ML lifecycle in one repository:

| Stage | What happens |
|---|---|
| 📥 **Data** | Public chest X-ray dataset (NORMAL / PNEUMONIA), loaded via `torchvision.datasets.ImageFolder` |
| 🧠 **Model** | 4-block custom CNN, trained end-to-end with Adam + cross-entropy loss |
| 🧪 **Evaluation** | Accuracy, precision, recall, F1, and confusion matrix on a held-out test split |
| 🌐 **Deployment** | Single-file Streamlit app with live inference, architecture insights, and metrics |

> ⚠️ **Disclaimer:** This is an educational / research project. It is **not a medical diagnostic tool** and should never be used for real clinical decisions. Always consult a qualified medical professional.

<br>

## ✨ Features

- 🔬 **Live classifier** — upload a JPG/PNG chest X-ray and get an instant NORMAL vs. PNEUMONIA prediction
- 📊 **Confidence breakdown** — full softmax probability distribution across both classes, not just a single label
- 🧱 **Transparent architecture** — a dedicated *Model Insights* tab exposes the exact CNN architecture, parameter count, and training configuration
- 📈 **Honest metrics** — evaluation numbers are only shown if a real `metrics.json` exists; the app never fabricates performance figures
- 🎛️ **Tabbed single-file app** — Home, Classifier, Model Insights, and About all live in one `app.py`, no multipage routing overhead
- 💻 **CPU/GPU aware** — automatically runs on CUDA when available, falls back to CPU otherwise

<br>

## 🧠 Model Architecture

A **custom CNN**, built and trained from scratch — no transfer learning — designed for 96×96 grayscale radiographs.

```
Input (1 × 96 × 96, grayscale)
        │
        ▼
 Conv Block 1   Conv2d(1 → 32,  3×3) → ReLU → MaxPool
        │
        ▼
 Conv Block 2   Conv2d(32 → 64,  3×3) → ReLU → MaxPool
        │
        ▼
 Conv Block 3   Conv2d(64 → 128, 3×3) → ReLU → MaxPool
        │
        ▼
 Conv Block 4   Conv2d(128 → 256, 3×3) → ReLU → MaxPool
        │
        ▼
 Global Avg Pool (Adaptive → 4×4)
        │
        ▼
      Flatten
        │
        ▼
 FC Head   4096 → 512 → 128 → 2   (ReLU between layers)
        │
        ▼
  Output logits (NORMAL, PNEUMONIA)
```

<div align="center">

| Property | Value |
|---|---|
| Input | 96 × 96, single-channel (grayscale) |
| Normalization | mean = 0.5, std = 0.5 |
| Output | 2-way softmax — `NORMAL`, `PNEUMONIA` |
| Loss function | Cross-Entropy Loss |
| Optimizer | Adam (lr = 0.001) |
| Epochs | 12 |
| Batch size | 64 |
| Data split | 70% train / 15% validation / 15% test |

</div>

<br>

## 🖥️ App Walkthrough

The Streamlit app is organized into four tabs:

<table>
<tr>
<td width="50%" valign="top">

### 🏠 Home
Project overview, a 5-card feature summary, and a visual "how it works" pipeline: **Upload → Preprocess → Model → Prediction → Confidence**.

### 🔬 Classifier
Drag-and-drop upload on the left, live prediction + probability bars on the right.

</td>
<td width="50%" valign="top">

### 📊 Model Insights
Full architecture breakdown, parameter count, training configuration, and real evaluation metrics (when available).

### ℹ️ About
Objective, tech stack, methodology, dataset source, and honest limitations.

</td>
</tr>
</table>

<br>

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![torchvision](https://img.shields.io/badge/torchvision-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

<br>

## 📂 Project Structure

```
Chest-XRay-Pneumonia-Classification/
│
├── app.py                          # Single-file Streamlit app (Home · Classifier · Insights · About)
│
├── src/
│   ├── model.py                    # XRayModel — the CNN architecture
│   ├── prediction.py               # Model/checkpoint loading + inference wrapper
│   ├── preprocessing.py            # Image loading & training-matched transform pipeline
│   ├── styles.py                   # Custom UI components (hero, cards, badges, probability bars)
│   └── utils.py                    # Shared constants & helpers
│
├── models/
│   ├── new_chest_xray_model_bht.pth        # Trained model weights
│   ├── new_chest_xray_checkpoint_bht.pth   # Training checkpoint
│   └── new_class_to_idx_bht.json           # Class-to-index mapping
│
├── notebooks/
│   └── Chest_X_Ray_Classification.ipynb    # Full training & evaluation notebook
│
├── data/
│   └── data.txt                    # Dataset source link (dataset not bundled — 1.2GB+)
│
├── graphs/                         # Training/evaluation plots
├── .streamlit/
│   └── config.toml                 # Streamlit theme configuration
│
└── requirements.txt
```

<br>

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Chest-XRay-Pneumonia-Classification.git
cd Chest-XRay-Pneumonia-Classification
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

> 💡 **Dataset:** The raw image dataset (1.2GB+) isn't bundled in this repo. Grab it from the [Kaggle Chest X-Ray Images dataset](https://www.kaggle.com/datasets/paulti/chest-xray-images) — see `data/data.txt` for details. You only need it if you want to retrain the model; the app itself ships with pretrained weights in `models/`.

<br>

## 📊 Evaluation

Model performance is computed on a held-out **15% test split** and reported inside the app's **Model Insights** tab via `models/metrics.json` — accuracy, precision, recall, F1-score, and a confusion matrix. If that file isn't present, the app transparently says so rather than showing placeholder numbers.

<br>

## ⚠️ Limitations

- Trained on a single public dataset — may not generalize to X-rays from different scanners, populations, or imaging protocols
- Binary classification only — does not localize findings or detect other thoracic conditions
- Sensitive to image quality; blurry, cropped, or non-chest-X-ray inputs can produce unreliable results
- A personal / educational project — **not** a validated or clinically approved diagnostic tool

<br>

## 🗺️ Roadmap

- [ ] Grad-CAM visualizations to highlight regions driving each prediction
- [ ] Data augmentation experiments to improve generalization
- [ ] Multi-class extension (bacterial vs. viral pneumonia)
- [ ] Model comparison against pretrained backbones (ResNet, DenseNet)

<br>

## 📄 License

This project is released for **educational and research purposes**. See the repository for license details.

<br>

<div align="center">

**Built with 🩻 + 🧠 by Harsh**

*If this project helped you, consider giving it a ⭐*

</div>