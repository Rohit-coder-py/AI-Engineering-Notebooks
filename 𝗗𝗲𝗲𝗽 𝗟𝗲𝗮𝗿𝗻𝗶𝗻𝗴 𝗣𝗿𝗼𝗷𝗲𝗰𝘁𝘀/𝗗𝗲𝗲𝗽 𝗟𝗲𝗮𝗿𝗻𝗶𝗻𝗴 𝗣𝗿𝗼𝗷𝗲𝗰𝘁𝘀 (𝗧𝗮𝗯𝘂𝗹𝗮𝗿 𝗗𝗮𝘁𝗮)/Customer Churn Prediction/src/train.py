"""
Full training pipeline - run this to retrain the model from scratch.

    python src/train.py

Reads data/cleaned_and_scaled_dataset.csv (same file the notebook exports),
trains the exact MyModel architecture from the notebook, and saves everything
the app needs into models/:

    churn_model_weights.npz   - trained weights (framework-agnostic, loaded
                                 into a torch model by src/infer.py)
    scaler.pkl                 - fitted StandardScaler
    feature_order.pkl          - exact column order the model expects
    metrics.json                - test-set metrics

Also drops evaluation plots into images/06_confusion_matrix.png and
images/07_roc_curve.png.
"""

import json
import os

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                              precision_score, recall_score, roc_auc_score,
                              roc_curve)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset

from model import MyModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_and_scaled_dataset.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

EPOCHS = 60
BATCH_SIZE = 64
LEARNING_RATE = 0.001
RANDOM_STATE = 42


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # ---- load data ----
    df = pd.read_csv(DATA_PATH)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    X = df.drop(columns=["Churn"])
    y = df["Churn"]
    feature_order = X.columns.tolist()

    # ---- same 70/15/15 split as the notebook ----
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=RANDOM_STATE, stratify=y)
    X_valid, X_test, y_valid, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=RANDOM_STATE, stratify=y_temp)

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_valid_s = scaler.transform(X_valid)
    X_test_s = scaler.transform(X_test)

    X_train_t = torch.tensor(X_train_s, dtype=torch.float32)
    X_valid_t = torch.tensor(X_valid_s, dtype=torch.float32)
    X_test_t = torch.tensor(X_test_s, dtype=torch.float32)

    y_train_t = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
    y_valid_t = torch.tensor(y_valid.values, dtype=torch.float32).view(-1, 1)
    y_test_t = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)

    train_loader = DataLoader(TensorDataset(X_train_t, y_train_t), batch_size=BATCH_SIZE, shuffle=True)

    # ---- model / loss / optimizer ----
    n_pos = y_train_t.sum()
    n_neg = len(y_train_t) - n_pos
    pos_weight = (n_neg / n_pos).clone().detach()

    model = MyModel(n_features=X_train_t.shape[1])
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # ---- training loop (same shape as the notebook's) ----
    model.train()
    for epoch in range(EPOCHS):
        epoch_loss = 0.0
        for X_batch, y_batch in train_loader:
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        avg_loss = epoch_loss / len(train_loader)
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"Epoch [{epoch + 1}/{EPOCHS}] | Loss: {avg_loss:.4f}")

    # ---- evaluate on test set ----
    model.eval()
    with torch.no_grad():
        logits = model(X_test_t).squeeze()
        probs = torch.sigmoid(logits).numpy()
    labels = y_test_t.squeeze().numpy()
    preds = (probs >= 0.5).astype(int)

    acc = accuracy_score(labels, preds)
    prec = precision_score(labels, preds, zero_division=0)
    rec = recall_score(labels, preds, zero_division=0)
    f1 = f1_score(labels, preds, zero_division=0)
    auc = roc_auc_score(labels, probs)

    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1       : {f1:.4f}")
    print(f"ROC-AUC  : {auc:.4f}")

    metrics = {
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "roc_auc": round(float(auc), 4),
        "test_size": int(len(labels)),
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "learning_rate": LEARNING_RATE,
        "pos_weight": round(float(pos_weight), 4),
    }
    with open(os.path.join(MODELS_DIR, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    # ---- save weights framework-agnostically (npz) so infer.py has one
    #      loading path regardless of whether the notebook or this script
    #      produced them ----
    state_dict = model.state_dict()
    weight_dict = {k: v.numpy() for k, v in state_dict.items()}
    np.savez(os.path.join(MODELS_DIR, "churn_model_weights.npz"), **weight_dict)

    joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.pkl"))
    joblib.dump(feature_order, os.path.join(MODELS_DIR, "feature_order.pkl"))

    print("Saved model weights, scaler, feature order, metrics to models/")

    # ---- evaluation plots ----
    sns.set_style("whitegrid")

    cm = confusion_matrix(labels, preds)
    fig, ax = plt.subplots(figsize=(5, 4.2))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["No Churn", "Churn"], yticklabels=["No Churn", "Churn"], ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix - Test Set")
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "06_confusion_matrix.png"), dpi=140)
    plt.close()

    fpr, tpr, _ = roc_curve(labels, probs)
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    ax.plot(fpr, tpr, color="#2563eb", lw=2, label=f"ROC curve (AUC = {auc:.3f})")
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve - Test Set")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "07_roc_curve.png"), dpi=140)
    plt.close()

    print("Saved evaluation plots to images/")


if __name__ == "__main__":
    main()
