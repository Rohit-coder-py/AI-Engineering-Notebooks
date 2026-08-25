# model.py will contain the definition of neural network


import torch
import torch.nn as nn

class OptunaShipSenseModel(nn.Module):

    def __init__(self, input_features, hidden1, hidden2, hidden3, dropout):

        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(input_features, hidden1),
            nn.ReLU(),
            nn.Dropout(dropout),

            nn.Linear(hidden1, hidden2),
            nn.ReLU(),
            nn.Dropout(dropout),

            nn.Linear(hidden2, hidden3),
            nn.ReLU(),
            nn.Dropout(dropout),

            nn.Linear(hidden3, 1)
        )

    def forward(self, x):

        return self.network(x)