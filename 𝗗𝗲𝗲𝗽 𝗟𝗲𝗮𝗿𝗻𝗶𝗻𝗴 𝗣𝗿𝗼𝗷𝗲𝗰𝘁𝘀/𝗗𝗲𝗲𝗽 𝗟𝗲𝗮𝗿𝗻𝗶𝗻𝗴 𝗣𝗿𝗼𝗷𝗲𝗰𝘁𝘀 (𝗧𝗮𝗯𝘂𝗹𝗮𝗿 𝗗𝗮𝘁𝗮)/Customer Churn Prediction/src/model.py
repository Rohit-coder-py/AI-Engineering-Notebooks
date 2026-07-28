"""
Same architecture as MyModel in notebooks/Customer Churn Prediction.ipynb.
Kept identical on purpose so the weights trained in the notebook can be
loaded here without any surprises.
"""

import torch
import torch.nn as nn


class MyModel(nn.Module):
    def __init__(self, n_features: int = 30):
        super().__init__()

        self.fc1 = nn.Linear(n_features, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 16)
        self.fc4 = nn.Linear(16, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)

        return x
