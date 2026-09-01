"""
Image preprocessing pipeline.

Copied exactly from the transform pipeline defined in
notebooks/Chest_X_Ray_Classification.ipynb (Cell 45):

    transforms.Compose([
        transforms.Resize((96, 96)),
        transforms.Grayscale(num_output_channels=1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5]),
    ])

Do not change these numbers without retraining -- the model was trained
on exactly this input distribution.
"""

from __future__ import annotations

import io

import torch
from PIL import Image, UnidentifiedImageError
from torchvision import transforms

IMAGE_SIZE = (96, 96)
NORMALIZE_MEAN = [0.5]
NORMALIZE_STD = [0.5]

_transform = transforms.Compose(
    [
        transforms.Resize(IMAGE_SIZE),
        transforms.Grayscale(num_output_channels=1),
        transforms.ToTensor(),
        transforms.Normalize(mean=NORMALIZE_MEAN, std=NORMALIZE_STD),
    ]
)


class InvalidImageError(Exception):
    """Raised when an uploaded file can't be read as a valid image."""


def load_image(file_bytes: bytes) -> Image.Image:
    """Open raw uploaded bytes as a PIL image, with friendly error handling."""
    try:
        image = Image.open(io.BytesIO(file_bytes))
        image.load()  # force-read pixel data now, so truncated files fail here
        return image
    except (UnidentifiedImageError, OSError) as exc:
        raise InvalidImageError(
            "That file couldn't be read as an image. Please upload a valid "
            "JPG, JPEG, or PNG chest X-ray."
        ) from exc


def preprocess(image: Image.Image) -> torch.Tensor:
    """Apply the training-time transform pipeline and add a batch dimension."""
    tensor = _transform(image)
    return tensor.unsqueeze(0)  # (1, 1, 96, 96)


def denormalize_for_display(tensor: torch.Tensor) -> torch.Tensor:
    """Undo the (mean=0.5, std=0.5) normalization, for debug/preview use."""
    return tensor * NORMALIZE_STD[0] + NORMALIZE_MEAN[0]
