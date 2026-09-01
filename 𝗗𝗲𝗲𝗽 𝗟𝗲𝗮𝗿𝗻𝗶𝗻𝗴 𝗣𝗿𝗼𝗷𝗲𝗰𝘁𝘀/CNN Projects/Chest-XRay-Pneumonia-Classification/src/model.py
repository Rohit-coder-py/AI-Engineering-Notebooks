"""
Model architecture for the Chest X-Ray Classifier.

IMPORTANT: This class is copied EXACTLY (layer for layer) from the
`X_ray_Model` class defined in notebooks/Chest_X_Ray_Classification.ipynb
so that saved weights (a state_dict) load into an identical graph.

If you ever change the architecture in the notebook, mirror the change
here too -- otherwise `load_state_dict` will fail with a shape/key
mismatch.
"""

import torch.nn as nn


class XRayModel(nn.Module):
    """Custom CNN for binary chest X-ray classification (NORMAL vs PNEUMONIA).

    Input:  grayscale image tensor, shape (batch, 1, 96, 96)
    Output: raw logits, shape (batch, 2)
    """

    def __init__(self) -> None:
        super().__init__()

        # Block 1
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2)

        # Block 2
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)

        # Block 3
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1)

        # Block 4
        self.conv4 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1)

        # Global average pool -> fixed 4x4 spatial size regardless of input size
        self.gap = nn.AdaptiveAvgPool2d((4, 4))

        self.flatten = nn.Flatten()

        # Fully connected head
        self.fc1 = nn.Linear(in_features=4 * 4 * 256, out_features=512)
        self.fc2 = nn.Linear(in_features=512, out_features=128)
        self.fc3 = nn.Linear(in_features=128, out_features=2)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)

        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)

        x = self.conv3(x)
        x = self.relu(x)
        x = self.pool(x)

        x = self.conv4(x)
        x = self.relu(x)
        x = self.pool(x)

        x = self.gap(x)
        x = self.flatten(x)

        x = self.fc1(x)
        x = self.relu(x)

        x = self.fc2(x)
        x = self.relu(x)

        x = self.fc3(x)
        return x


# Kept as an alias so a raw `torch.save(model, ...)` (whole-object) pickle
# saved from inside the original notebook can still unpickle successfully,
# since that notebook defines the class as `X_ray_Model`.
X_ray_Model = XRayModel
