"""
Full training pipeline — reproduces the notebook end-to-end so the
model can be retrained from scratch.

Usage:
    python src/train.py --data data/credit_card_frauds_cleaned.csv --models models

Note: this mirrors the notebook's original training configuration
exactly (plain BCEWithLogitsLoss, no class weighting, 10 epochs) so
the results match `models/metrics.json`. See the notebook's
"Conclusion & Next Steps" section for ideas on improving recall.
"""

import argparse
import json
import os

import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                              recall_score, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from torch.utils.data import DataLoader, TensorDataset

from model import FraudDetectionModel
from preprocessing import clean_raw


def main(data_path: str, models_dir: str, epochs: int = 10, batch_size: int = 64, lr: float = 1e-3):
    os.makedirs(models_dir, exist_ok=True)

    df = pd.read_csv(data_path)
    df = clean_raw(df)  # no-op if already cleaned

    X = df.drop("is_fraud", axis=1)
    y = df["is_fraud"]

    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    X_valid, X_test, y_valid, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
    )

    categorical_columns = X_train.select_dtypes(include="object").columns
    numerical_columns = X_train.select_dtypes(include=["number"]).columns

    encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    X_train[categorical_columns] = encoder.fit_transform(X_train[categorical_columns])
    X_valid[categorical_columns] = encoder.transform(X_valid[categorical_columns])
    X_test[categorical_columns] = encoder.transform(X_test[categorical_columns])

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

    train_loader = DataLoader(TensorDataset(X_train_t, y_train_t), batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(TensorDataset(X_test_t, y_test_t), batch_size=batch_size, shuffle=False)

    model = FraudDetectionModel(n_features=X_train_t.shape[1])
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    model.train()
    for epoch in range(epochs):
        epoch_loss = 0.0
        for X_batch, y_batch in train_loader:
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        print(f"Epoch [{epoch + 1}/{epochs}] | Loss: {epoch_loss / len(train_loader):.6f}")

    model.eval()
    all_logits, all_labels = [], []
    with torch.no_grad():
        for X_batch, y_batch in test_loader:
            all_logits.append(model(X_batch))
            all_labels.append(y_batch)
    probs = torch.sigmoid(torch.cat(all_logits).squeeze()).numpy()
    labels = torch.cat(all_labels).squeeze().numpy()
    preds = (probs >= 0.5).astype(int)

    metrics = {
        "accuracy": float(accuracy_score(labels, preds)),
        "precision": float(precision_score(labels, preds, zero_division=0)),
        "recall": float(recall_score(labels, preds, zero_division=0)),
        "f1_score": float(f1_score(labels, preds, zero_division=0)),
        "roc_auc": float(roc_auc_score(labels, probs)),
        "test_size": int(len(labels)),
        "fraud_in_test": int(labels.sum()),
        "threshold": 0.5,
    }
    print(json.dumps(metrics, indent=2))

    torch.save(model.state_dict(), f"{models_dir}/fraud_model.pth")
    joblib.dump(encoder, f"{models_dir}/encoder.pkl")
    joblib.dump(scaler, f"{models_dir}/scaler.pkl")
    joblib.dump(list(categorical_columns), f"{models_dir}/categorical_columns.pkl")
    joblib.dump(list(numerical_columns), f"{models_dir}/numerical_columns.pkl")
    joblib.dump(list(X.columns), f"{models_dir}/feature_order.pkl")
    with open(f"{models_dir}/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nSaved model + preprocessing artifacts to {models_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/credit_card_frauds_cleaned.csv")
    parser.add_argument("--models", default="models")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=1e-3)
    args = parser.parse_args()
    main(args.data, args.models, args.epochs, args.batch_size, args.lr)
