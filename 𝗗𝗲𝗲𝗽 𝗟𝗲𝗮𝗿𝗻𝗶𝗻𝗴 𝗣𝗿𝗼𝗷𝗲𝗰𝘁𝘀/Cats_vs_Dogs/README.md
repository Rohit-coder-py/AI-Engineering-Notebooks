# Cats vs Dogs

Binary image classifier (Cat / Dog) built with a CNN in PyTorch, deployed as a Streamlit app.

```
Business Understanding
        ↓
Data Collection
        ↓
Dataset Understanding
        ↓
Data Cleaning (Remove corrupted images)
        ↓
Train / Validation / Test Split
        ↓
Image Transformations
        ↓
Create Dataset (ImageFolder)
        ↓
Create DataLoaders
        ↓
Visualize Images
        ↓
Design CNN Architecture
        ↓
Choose Loss Function
        ↓
Choose Optimizer
        ↓
Training Loop
        ↓
Validation
        ↓
Model Evaluation
        ↓
Save Trained Model
        ↓
Inference / Prediction
        ↓
Deployment (Streamlit)
```

## Dataset

Uses the standard **Dogs vs Cats** dataset (Kaggle / Microsoft Cats & Dogs), expected as:

```
PetImages/
├── Cat/
└── Dog/
```

The dataset itself isn't in this folder (it's ~800MB of images, and the original notebook
points at a local path on your machine). Download it and update the `dataset_path` in the
notebook, or pass it to `train.py --data`.

## Project structure

```
Cats_vs_Dogs/
├── Cats_vs_Dogs.ipynb   # full pipeline notebook (your original + completed steps)
├── train.py             # script version of the notebook, for CLI (re)training
├── app.py                # Streamlit app - upload an image, get a prediction
├── src/
│   ├── model.py          # CatDogCNN class + shared transform (imported everywhere)
│   └── infer.py           # load_model() / predict_image(), used by app.py
├── models/                # trained weights land here (cat_dog_cnn.pth)
├── requirements.txt
└── README.md
```

## Model

`CatDogCNN`: 4 conv blocks (32 → 64 → 128 → 256 channels, each Conv2d + ReLU + MaxPool)
→ Flatten → FC(512) → FC(128) → FC(2). Input is 224×224 RGB, ImageNet-normalized.
Loss: CrossEntropyLoss. Optimizer: Adam (lr=0.001).

## Setup

```bash
pip install -r requirements.txt
```

## Train

Either run `Cats_vs_Dogs.ipynb` top to bottom, or from the terminal:

```bash
python train.py --data "C:\Users\shobh\Downloads\PetImages" --epochs 10
```

Both write the trained weights to `models/cat_dog_cnn.pth`.

## Run the app

```bash
streamlit run app.py
```

Upload an image and the app shows the predicted class with a confidence breakdown.
If `models/cat_dog_cnn.pth` isn't there yet, the app tells you to train first instead
of failing silently.

## Notes

- `models/` and `*.pth` are gitignored, same as your original `.gitignore` - the model
  needs to be trained locally (or you can remove that line before pushing if you want
  the weights in the repo).
- The notebook's original training loop was left as-is; the completed version (with
  validation, evaluation, saving, and inference) was added as new cells after it, same
  as how you iterated on the Azure cost project.
