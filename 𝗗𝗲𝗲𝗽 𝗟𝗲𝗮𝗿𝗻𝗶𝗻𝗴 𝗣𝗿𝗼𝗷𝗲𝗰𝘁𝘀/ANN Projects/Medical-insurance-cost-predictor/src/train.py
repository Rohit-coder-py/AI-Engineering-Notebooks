import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from preprocessing import load_data, clean_data, get_feature_types, fit_transform, save_artifacts, TARGET_COLUMN
from model import InsuranceANN

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "medical_insurance_cost.csv")
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
MODELS_DIR = os.path.join(BASE_DIR, "models")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

EPOCHS = 100
BATCH_SIZE = 64
LEARNING_RATE = 0.001

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("using device:", device)

df = load_data(DATA_PATH)
df = clean_data(df)

X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_valid, X_test, y_valid, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

print("training set  :", X_train.shape)
print("validation set:", X_valid.shape)
print("testing set   :", X_test.shape)

categorical_columns, numerical_columns = get_feature_types(X_train)

X_train_final, X_valid_final, X_test_final, encoder, scaler, feature_order = fit_transform(
    X_train, X_valid, X_test, categorical_columns, numerical_columns
)

feature_meta = {
    "numerical_columns": numerical_columns,
    "categorical_columns": categorical_columns,
    "feature_order": feature_order,
}
save_artifacts(encoder, scaler, feature_meta, ARTIFACTS_DIR)

X_train_tensor = torch.tensor(X_train_final, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)

X_valid_tensor = torch.tensor(X_valid_final, dtype=torch.float32).to(device)
y_valid_tensor = torch.tensor(y_valid.values, dtype=torch.float32).view(-1, 1).to(device)

X_test_tensor = torch.tensor(X_test_final, dtype=torch.float32).to(device)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

model = InsuranceANN(input_dim=X_train_final.shape[1]).to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

train_losses = []
valid_losses = []

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0

    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)

        optimizer.zero_grad()
        preds = model(X_batch)
        loss = criterion(preds, y_batch)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * X_batch.size(0)

    epoch_train_loss = running_loss / len(train_dataset)
    train_losses.append(epoch_train_loss)

    model.eval()
    with torch.no_grad():
        valid_preds = model(X_valid_tensor)
        epoch_valid_loss = criterion(valid_preds, y_valid_tensor).item()
        valid_losses.append(epoch_valid_loss)

    if (epoch + 1) % 10 == 0:
        print(f"epoch {epoch + 1}/{EPOCHS} - train loss: {epoch_train_loss:.2f} - valid loss: {epoch_valid_loss:.2f}")

torch.save(model.state_dict(), os.path.join(MODELS_DIR, "medical_insurance_ann.pth"))
print("model saved to", os.path.join(MODELS_DIR, "medical_insurance_ann.pth"))

plt.figure(figsize=(8, 5))
plt.plot(train_losses, label="train loss")
plt.plot(valid_losses, label="validation loss")
plt.xlabel("epoch")
plt.ylabel("mse loss")
plt.title("training loss curve")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "06_training_loss.png"))
plt.close()

model.eval()
with torch.no_grad():
    test_preds = model(X_test_tensor).cpu().numpy().flatten()

y_test_actual = y_test.values

mae = mean_absolute_error(y_test_actual, test_preds)
rmse = np.sqrt(mean_squared_error(y_test_actual, test_preds))
r2 = r2_score(y_test_actual, test_preds)

print("test mae :", mae)
print("test rmse:", rmse)
print("test r2  :", r2)

plt.figure(figsize=(7, 7))
plt.scatter(y_test_actual, test_preds, alpha=0.4, color="#2563EB")
plt.plot(
    [y_test_actual.min(), y_test_actual.max()],
    [y_test_actual.min(), y_test_actual.max()],
    color="red",
    linestyle="--",
)
plt.xlabel("actual annual medical cost")
plt.ylabel("predicted annual medical cost")
plt.title("actual vs predicted")
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "07_actual_vs_predicted.png"))
plt.close()

residuals = y_test_actual - test_preds

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].scatter(test_preds, residuals, alpha=0.4, color="#16A34A")
axes[0].axhline(0, color="red", linestyle="--")
axes[0].set_xlabel("predicted value")
axes[0].set_ylabel("residual")
axes[0].set_title("residuals vs predicted")

axes[1].hist(residuals, bins=50, color="#F97316")
axes[1].set_xlabel("residual")
axes[1].set_title("residual distribution")

plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "08_residual_analysis.png"))
plt.close()

print("done")
