

import sys
import os
sys.path.append(os.path.dirname(__file__))

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc
)

from preprocessing import (
    load_data, clean_data, encode_categoricals, get_feature_target,
    fit_scaler, apply_scaler, save_artifacts, NUMERICAL_COLS
)
from model import AddictionANN

# ---------------------------------------------------------------------------
# Paths & config
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "Smartphone_Usage_And_Addiction_Analysis_7500_Rows.csv")
IMAGES_DIR = os.path.join(ROOT, "images")
MODELS_DIR = os.path.join(ROOT, "models")
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

SEED = 42
np.random.seed(SEED)
torch.manual_seed(SEED)

# Dark editorial plotting theme, matching the rest of the portfolio
BG = "#0d0f14"
PANEL = "#161923"
GOLD = "#c9a86a"
EMERALD = "#2f6f5e"
OXBLOOD = "#7a2e2e"
TEXT = "#e7e2d6"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": PANEL,
    "axes.edgecolor": "#3a3f4d",
    "axes.labelcolor": TEXT,
    "text.color": TEXT,
    "xtick.color": TEXT,
    "ytick.color": TEXT,
    "grid.color": "#2a2e3a",
    "font.family": "monospace",
})


def save_fig(name):
    path = os.path.join(IMAGES_DIR, name)
    plt.savefig(path, dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"  saved {name}")


# ---------------------------------------------------------------------------
# Phase 3-5: Understanding, Cleaning, EDA
# ---------------------------------------------------------------------------
print("=" * 60)
print("PHASE 3-5: DATA UNDERSTANDING, CLEANING & EDA")
print("=" * 60)

df_raw = load_data(DATA_PATH)
print(f"Raw shape: {df_raw.shape}")
print(f"Missing values:\n{df_raw.isnull().sum()[df_raw.isnull().sum() > 0]}")
print(f"Duplicates: {df_raw.duplicated().sum()}")

df = clean_data(df_raw)
print(f"Cleaned shape (after dropping IDs + leakage col + dupes): {df.shape}")

# Target distribution
plt.figure(figsize=(5, 4))
sns.countplot(x="addicted_label", data=df, palette=[EMERALD, GOLD])
plt.title("Target Distribution: Addicted Label", color=TEXT)
plt.xlabel("Addicted (0 = No, 1 = Yes)")
save_fig("01_target_distribution.png")

# Numerical feature distributions
fig, axes = plt.subplots(3, 3, figsize=(14, 10))
for ax, col in zip(axes.flat, NUMERICAL_COLS):
    sns.histplot(df[col], kde=True, color=GOLD, ax=ax)
    ax.set_title(col, color=TEXT, fontsize=9)
plt.tight_layout()
save_fig("02_numerical_distributions.png")

# Correlation heatmap
plt.figure(figsize=(9, 7))
corr = df[NUMERICAL_COLS + ["addicted_label"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdGy_r", center=0,
            linewidths=0.5, linecolor=BG)
plt.title("Feature Correlation Matrix", color=TEXT)
save_fig("03_correlation_heatmap.png")

# Categorical vs target
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, col in zip(axes, ["gender", "stress_level", "academic_work_impact"]):
    sns.countplot(x=col, hue="addicted_label", data=df, ax=ax,
                  palette=[EMERALD, OXBLOOD])
    ax.set_title(f"{col} vs Addiction", color=TEXT, fontsize=10)
plt.tight_layout()
save_fig("04_categorical_vs_target.png")

print("\nKey EDA insight: 'social_media_hours' and 'daily_screen_time_hours'")
print("show the strongest positive relationship with addicted_label; sleep_hours")
print("shows a negative relationship. addiction_level was dropped as direct leakage.")

# ---------------------------------------------------------------------------
# Phase 6-8: Feature Engineering, Prep, Tensors
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("PHASE 6-8: FEATURE ENGINEERING & PREP")
print("=" * 60)

df_encoded, encoders = encode_categoricals(df)
X, y = get_feature_target(df_encoded)
feature_order = list(X.columns)
print(f"Final feature count: {len(feature_order)}")
print(f"Features: {feature_order}")

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=SEED
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=SEED
)
print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")

scaler = fit_scaler(X_train)
X_train_s = apply_scaler(X_train, scaler)
X_val_s = apply_scaler(X_val, scaler)
X_test_s = apply_scaler(X_test, scaler)

save_artifacts(scaler, encoders, feature_order, MODELS_DIR)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def to_loader(X_df, y_arr, batch_size, shuffle):
    X_t = torch.tensor(X_df.values, dtype=torch.float32)
    y_t = torch.tensor(y_arr, dtype=torch.float32).unsqueeze(1)
    ds = TensorDataset(X_t, y_t)
    return DataLoader(ds, batch_size=batch_size, shuffle=shuffle)


X_val_t = torch.tensor(X_val_s.values, dtype=torch.float32).to(device)
y_val_t = torch.tensor(y_val, dtype=torch.float32).unsqueeze(1).to(device)
X_test_t = torch.tensor(X_test_s.values, dtype=torch.float32).to(device)
y_test_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1).to(device)

# ---------------------------------------------------------------------------
# Phase 9-15: Model, Loss, Optimizer, Training loop, Hyperparameter search
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("PHASE 9-15: MODEL BUILD, TRAINING & HYPERPARAMETER SEARCH")
print("=" * 60)

# Class imbalance (0: 2192, 1: 5308) -> weighted loss
pos_weight = torch.tensor([len(y_train[y_train == 0]) / len(y_train[y_train == 1])]).to(device)

configs = [
    {"name": "baseline",   "hidden_dims": (64, 32),     "lr": 1e-3, "dropout": 0.3, "batch_size": 64},
    {"name": "deeper",     "hidden_dims": (128, 64, 32), "lr": 1e-3, "dropout": 0.3, "batch_size": 64},
    {"name": "wide_lowlr", "hidden_dims": (64, 32, 16), "lr": 5e-4, "dropout": 0.2, "batch_size": 32},
]

EPOCHS = 60
results = []

for cfg in configs:
    print(f"\n--- Training config: {cfg['name']} {cfg} ---")
    torch.manual_seed(SEED)
    model = AddictionANN(input_dim=X_train_s.shape[1],
                          hidden_dims=cfg["hidden_dims"],
                          dropout=cfg["dropout"]).to(device)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg["lr"])
    train_loader = to_loader(X_train_s, y_train, cfg["batch_size"], shuffle=True)

    history = []
    for epoch in range(EPOCHS):
        model.train()
        epoch_loss = 0.0
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            logits = model(xb)
            loss = criterion(logits, yb)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * xb.size(0)
        epoch_loss /= len(train_loader.dataset)
        history.append(epoch_loss)
        if (epoch + 1) % 20 == 0:
            print(f"  epoch {epoch+1}/{EPOCHS}  loss={epoch_loss:.4f}")

    model.eval()
    with torch.no_grad():
        val_logits = model(X_val_t)
        val_probs = torch.sigmoid(val_logits).cpu().numpy().ravel()
        val_preds = (val_probs >= 0.5).astype(int)
    val_acc = accuracy_score(y_val, val_preds)
    val_f1 = f1_score(y_val, val_preds)
    print(f"  -> val_acc={val_acc:.4f}  val_f1={val_f1:.4f}")

    results.append({
        "config": cfg, "model": model, "history": history,
        "val_acc": val_acc, "val_f1": val_f1,
    })

best = max(results, key=lambda r: r["val_f1"])
print(f"\nBest config by validation F1: {best['config']['name']} "
      f"(val_f1={best['val_f1']:.4f}, val_acc={best['val_acc']:.4f})")

# Loss curves for all configs
plt.figure(figsize=(7, 5))
colors = [GOLD, EMERALD, OXBLOOD]
for r, c in zip(results, colors):
    plt.plot(r["history"], label=r["config"]["name"], color=c)
plt.xlabel("Epoch")
plt.ylabel("Training Loss")
plt.title("Training Loss by Configuration", color=TEXT)
plt.legend()
save_fig("05_training_loss_curves.png")

# ---------------------------------------------------------------------------
# Phase 14: Final evaluation on held-out test set
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("PHASE 14: FINAL TEST SET EVALUATION")
print("=" * 60)

best_model = best["model"]
best_model.eval()
with torch.no_grad():
    test_logits = best_model(X_test_t)
    test_probs = torch.sigmoid(test_logits).cpu().numpy().ravel()
    test_preds = (test_probs >= 0.5).astype(int)

acc = accuracy_score(y_test, test_preds)
prec = precision_score(y_test, test_preds)
rec = recall_score(y_test, test_preds)
f1 = f1_score(y_test, test_preds)
cm = confusion_matrix(y_test, test_preds)
report = classification_report(y_test, test_preds)

print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"\nConfusion Matrix:\n{cm}")
print(f"\nClassification Report:\n{report}")

# Confusion matrix plot
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="RdGy_r",
            xticklabels=["Not Addicted", "Addicted"],
            yticklabels=["Not Addicted", "Addicted"])
plt.title("Confusion Matrix (Test Set)", color=TEXT)
plt.ylabel("Actual")
plt.xlabel("Predicted")
save_fig("06_confusion_matrix.png")

# ROC curve
fpr, tpr, _ = roc_curve(y_test, test_probs)
roc_auc = auc(fpr, tpr)
plt.figure(figsize=(5, 4))
plt.plot(fpr, tpr, color=GOLD, label=f"AUC = {roc_auc:.3f}")
plt.plot([0, 1], [0, 1], color="#555555", linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve (Test Set)", color=TEXT)
plt.legend()
save_fig("07_roc_curve.png")

# ---------------------------------------------------------------------------
# Phase 16: Save final model
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("PHASE 16: SAVING FINAL MODEL")
print("=" * 60)

torch.save({
    "model_state_dict": best_model.state_dict(),
    "input_dim": X_train_s.shape[1],
    "hidden_dims": best["config"]["hidden_dims"],
    "dropout": best["config"]["dropout"],
}, os.path.join(MODELS_DIR, "addiction_model.pth"))

metrics = {
    "accuracy": acc, "precision": prec, "recall": rec,
    "f1": f1, "roc_auc": roc_auc, "best_config": best["config"]["name"],
}
import json
with open(os.path.join(MODELS_DIR, "metrics.json"), "w") as f:
    json.dump(metrics, f, indent=2)

print(f"Saved model to {MODELS_DIR}/addiction_model.pth")
print(f"Saved metrics to {MODELS_DIR}/metrics.json")
print("\nDONE.")
