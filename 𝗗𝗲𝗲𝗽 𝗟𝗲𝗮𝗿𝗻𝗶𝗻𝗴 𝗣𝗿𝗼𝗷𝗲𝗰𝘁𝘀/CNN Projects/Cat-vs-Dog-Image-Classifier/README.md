---

#### **Try it out** : https://cat-vs-dog-image-classifier-pytorch-live.streamlit.app/
---



# 🐾 Cats vs Dogs — CNN Image Classifier

A binary image classifier that tells cats and dogs apart, built from scratch with a custom
CNN in PyTorch and shipped as an interactive Streamlit app.

| | |
|---|---|
| **Task** | Binary image classification (Cat / Dog) |
| **Framework** | PyTorch |
| **Test Accuracy** | **86.03%** |
| **Deployment** | Streamlit web app |

---

## Overview

This project covers the full lifecycle of a computer vision model — from raw, unverified
image data to a deployed inference app:

```
Data Collection → Cleaning → Train/Val/Test Split → Transforms
    → CNN Design → Training & Validation → Test Evaluation
    → Model Saving → Inference → Streamlit Deployment
```

The model is a 4-block convolutional network trained on the standard **Dogs vs Cats**
dataset, evaluated on a held-out test set, and served through a Streamlit UI where a user
uploads an image and gets back a predicted class with a confidence score.

## Results

Trained for 5 epochs on a 70/15/15 train/validation/test split (25,000 images total).

**Validation accuracy by epoch:**

| Epoch | Train Loss | Val Loss | Val Accuracy |
|:-----:|:----------:|:--------:|:-------------:|
| 1 | 0.6215 | 0.5089 | 75.42% |
| 2 | 0.4723 | 0.4022 | 82.07% |
| 3 | 0.3729 | 0.3767 | 83.41% |
| 4 | 0.3069 | 0.3004 | 87.10% |
| 5 | 0.2454 | 0.2873 | 87.55% |

**Test set (3,745 held-out images):**

```
              precision    recall  f1-score   support

         Cat       0.92      0.79      0.85      1874
         Dog       0.81      0.93      0.87      1871

    accuracy                           0.86      3745
```

The model is more precise on Cat (fewer false positives) but has higher recall on Dog
(catches more true dogs) — it slightly over-predicts "Dog" on borderline images.

## Model Architecture

`CatDogCNN` — a 4-block convolutional network with global average pooling to keep the
classifier head lightweight:

```
Input (3 × 96 × 96, ImageNet-normalized)
   → [Conv2d(3→32)  + ReLU + MaxPool]
   → [Conv2d(32→64) + ReLU + MaxPool]
   → [Conv2d(64→128) + ReLU + MaxPool]
   → [Conv2d(128→256) + ReLU + MaxPool]
   → AdaptiveAvgPool2d(4×4)
   → Flatten (4096)
   → FC(512) → ReLU → FC(128) → ReLU → FC(2)
```

- **Loss:** CrossEntropyLoss
- **Optimizer:** Adam (lr = 0.001)
- **Why global average pooling:** collapses the 4×4×256 feature map before the first
  fully-connected layer, cutting `fc1` from ~25.7M params down to ~2.1M — faster to train
  with negligible accuracy cost.

## Project Structure

```
Cats_vs_Dogs/
├── Cats_vs_Dogs.ipynb      # end-to-end notebook: EDA → training → evaluation → inference
├── train.py                # CLI script — clean, split, train, evaluate, save
├── app.py                  # Streamlit inference app
├── src/
│   ├── model.py             # CatDogCNN definition + shared transform pipeline
│   └── infer.py              # load_model() / predict_image(), used by app.py
├── models/
│   └── cat_dog_cnn.pth      # trained weights (gitignored — see Notes)
├── images/
│   └── Dataset_Visualization.png
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Get the dataset

This uses the standard **Dogs vs Cats** dataset (Kaggle / Microsoft Cats & Dogs Dataset).
It's not included in this repo (~800 MB). Download it and lay it out as:

```
PetImages/
├── Cat/
└── Dog/
```

### 3. Train

Either run `Cats_vs_Dogs.ipynb` top to bottom, or use the CLI:

```bash
python train.py --data "path/to/PetImages" --epochs 10
```

| Flag | Default | Description |
|---|---|---|
| `--data` | *required* | Path to raw `PetImages/` folder |
| `--split-output` | `PetImages_Splitted` | Where the train/val/test split is written |
| `--epochs` | `10` | Training epochs |
| `--batch-size` | `32` | Batch size |
| `--lr` | `0.001` | Learning rate (Adam) |
| `--skip-split` | off | Reuse an existing split instead of re-splitting |
| `--out` | `models/cat_dog_cnn.pth` | Output path for trained weights |

Both routes clean corrupted images, split the data 70/15/15, train with validation
tracked per epoch, evaluate on the test set (accuracy, precision/recall/F1, confusion
matrix), and save the weights to `models/cat_dog_cnn.pth`.

### 4. Run the app

```bash
streamlit run app.py
```

Upload a `.jpg` / `.jpeg` / `.png` image and the app returns the predicted class with a
Cat/Dog confidence breakdown. If no trained weights are found yet, the app shows setup
instructions instead of failing silently.

## Notes

- `models/` and `*.pth` are gitignored — weights need to be trained locally, or you can
  drop that line from `.gitignore` before pushing if you want them versioned.
- `src/model.py` is the single source of truth for the architecture and the image
  transform pipeline — the notebook, `train.py`, and `app.py` all import from it, so
  train/inference preprocessing can never drift out of sync.