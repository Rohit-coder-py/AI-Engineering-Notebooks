
import torch
import torch.nn as nn


class AddictionANN(nn.Module):
    def __init__(self, input_dim: int, hidden_dims=(64, 32, 16), dropout=0.3):
        super().__init__()

        layers = []
        prev_dim = input_dim
        for h in hidden_dims:
            layers.append(nn.Linear(prev_dim, h))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            prev_dim = h

        layers.append(nn.Linear(prev_dim, 1))  # raw logit output

        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)
