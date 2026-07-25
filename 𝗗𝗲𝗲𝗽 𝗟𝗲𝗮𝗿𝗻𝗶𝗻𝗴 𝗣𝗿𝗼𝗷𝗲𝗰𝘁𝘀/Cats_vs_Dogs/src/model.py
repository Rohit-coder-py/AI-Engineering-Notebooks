"""
CatDogCNN - same architecture designed in Cats_vs_Dogs.ipynb

pulled out here so the notebook, train.py, and app.py can all
import one shared definition instead of copy-pasting the class.
"""

import torch.nn as nn


class CatDogCNN(nn.Module):

    def __init__(self):
        super().__init__()

        # ==========================
        # First Convolution Block
        # ==========================
        self.conv1 = nn.Conv2d(
            in_channels=3,
            out_channels=32,
            kernel_size=3,
            padding=1
        )

        # Activation Function
        self.relu = nn.ReLU()

        # Pooling Layer
        self.pool = nn.MaxPool2d(kernel_size=2)

        # ==========================
        # Second Convolution Block
        # ==========================
        self.conv2 = nn.Conv2d(
            in_channels=32,
            out_channels=64,
            kernel_size=3,
            padding=1
        )

        # ==========================
        # Third Convolution Block
        # ==========================
        self.conv3 = nn.Conv2d(
            in_channels=64,
            out_channels=128,
            kernel_size=3,
            padding=1
        )

        # ==========================
        # Fourth Convolution Block
        # ==========================
        self.conv4 = nn.Conv2d(
            in_channels=128,
            out_channels=256,
            kernel_size=3,
            padding=1
        )

        # ==========================
        # Flatten Layer
        # ==========================
        self.flatten = nn.Flatten()

        # ==========================
        # Fully Connected Layers
        # ==========================
        self.fc1 = nn.Linear(
            in_features=50176,      # 256 x 14 x 14
            out_features=512
        )

        self.fc2 = nn.Linear(
            in_features=512,
            out_features=128
        )

        self.fc3 = nn.Linear(
            in_features=128,
            out_features=2
        )

    def forward(self, x):

        # ==========================
        # First Convolution Block
        # ==========================
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)

        # ==========================
        # Second Convolution Block
        # ==========================
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)

        # ==========================
        # Third Convolution Block
        # ==========================
        x = self.conv3(x)
        x = self.relu(x)
        x = self.pool(x)

        # ==========================
        # Fourth Convolution Block
        # ==========================
        x = self.conv4(x)
        x = self.relu(x)
        x = self.pool(x)

        # ==========================
        # Flatten
        # ==========================
        x = self.flatten(x)

        # ==========================
        # Fully Connected Layers
        # ==========================
        x = self.fc1(x)
        x = self.relu(x)

        x = self.fc2(x)
        x = self.relu(x)

        x = self.fc3(x)

        return x


# same transform pipeline used everywhere (notebook, train.py, app.py)
# kept here so all three always match

from torchvision import transforms

inference_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

CLASS_NAMES = ["Cat", "Dog"]
