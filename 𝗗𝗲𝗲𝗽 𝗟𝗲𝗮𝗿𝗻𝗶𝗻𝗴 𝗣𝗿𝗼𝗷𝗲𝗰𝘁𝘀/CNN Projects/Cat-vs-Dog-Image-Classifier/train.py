"""
train.py - script version of Cats_vs_Dogs.ipynb

Does the same steps as the notebook (clean -> split -> transform ->
dataloaders -> train -> validate -> evaluate -> save) so the model
can be (re)trained from the command line instead of cell by cell.

Usage:
    python train.py --data "C:\\Users\\shobh\\Downloads\\PetImages"

The raw PetImages/ folder needs a Cat/ and Dog/ subfolder inside it
(this is the standard Kaggle "Dogs vs Cats" layout). The script
creates the train/validation/test split itself, same as the notebook.
"""

import argparse
import os
import random
import shutil

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

from src.model import CatDogCNN, inference_transform


def clean_corrupted_images(dataset_path):
    corrupted_images = []

    for category in ["Cat", "Dog"]:
        folder = os.path.join(dataset_path, category)
        for image_name in os.listdir(folder):
            image_path = os.path.join(folder, image_name)
            try:
                with Image.open(image_path) as img:
                    img.verify()
            except Exception:
                corrupted_images.append(image_path)

    print(f"Corrupted Images Found: {len(corrupted_images)}")
    for file_path in corrupted_images:
        os.remove(file_path)


def split_dataset(dataset_path, output_path, train_ratio=0.70, val_ratio=0.15):
    for split in ["train", "validation", "test"]:
        for category in ["Cat", "Dog"]:
            os.makedirs(os.path.join(output_path, split, category), exist_ok=True)

    for category in ["Cat", "Dog"]:
        category_path = os.path.join(dataset_path, category)

        images = [
            img for img in os.listdir(category_path)
            if img.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
        random.shuffle(images)

        total_images = len(images)
        train_end = int(total_images * train_ratio)
        val_end = train_end + int(total_images * val_ratio)

        train_images = images[:train_end]
        val_images = images[train_end:val_end]
        test_images = images[val_end:]

        for image in train_images:
            shutil.copy(os.path.join(category_path, image), os.path.join(output_path, "train", category))
        for image in val_images:
            shutil.copy(os.path.join(category_path, image), os.path.join(output_path, "validation", category))
        for image in test_images:
            shutil.copy(os.path.join(category_path, image), os.path.join(output_path, "test", category))

        print(f"{category} completed.")

    print("\nDataset split completed successfully!")


def main():
    parser = argparse.ArgumentParser(description="Train the Cat vs Dog CNN")
    parser.add_argument("--data", required=True, help="path to raw PetImages folder (with Cat/ and Dog/ inside)")
    parser.add_argument("--split-output", default="PetImages_Splitted", help="where to write the train/val/test split")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--skip-split", action="store_true", help="use if --split-output already has train/validation/test folders")
    parser.add_argument("--out", default="models/cat_dog_cnn.pth")
    args = parser.parse_args()

    # ==========================
    # Data Cleaning + Split
    # ==========================
    if not args.skip_split:
        clean_corrupted_images(args.data)
        split_dataset(args.data, args.split_output)

    # ==========================
    # Datasets + Loaders
    # ==========================
    train_dataset = ImageFolder(root=os.path.join(args.split_output, "train"), transform=inference_transform)
    validation_dataset = ImageFolder(root=os.path.join(args.split_output, "validation"), transform=inference_transform)
    test_dataset = ImageFolder(root=os.path.join(args.split_output, "test"), transform=inference_transform)

    print("Train Images      :", len(train_dataset))
    print("Validation Images :", len(validation_dataset))
    print("Test Images       :", len(test_dataset))

    class_names = train_dataset.classes

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    validation_loader = DataLoader(validation_dataset, batch_size=args.batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)

    # ==========================
    # Model / Loss / Optimizer
    # ==========================
    model = CatDogCNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    # ==========================
    # Training + Validation
    # ==========================
    for epoch in range(args.epochs):
        model.train()
        running_loss = 0.0

        for images, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        epoch_train_loss = running_loss / len(train_loader)

        model.eval()
        val_running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for images, labels in validation_loader:
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_running_loss += loss.item()

                _, predicted = torch.max(outputs, 1)
                correct += (predicted == labels).sum().item()
                total += labels.size(0)

        epoch_val_loss = val_running_loss / len(validation_loader)
        epoch_val_acc = correct / total

        print(f"Epoch [{epoch+1}/{args.epochs}]  Train Loss: {epoch_train_loss:.4f}  Val Loss: {epoch_val_loss:.4f}  Val Acc: {epoch_val_acc*100:.2f}%")

    # ==========================
    # Test Evaluation
    # ==========================
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            all_preds.extend(predicted.numpy())
            all_labels.extend(labels.numpy())

    test_accuracy = (np.array(all_preds) == np.array(all_labels)).mean()
    print(f"\nTest Accuracy: {test_accuracy*100:.2f}%\n")
    print(classification_report(all_labels, all_preds, target_names=class_names))
    print("Confusion Matrix:")
    print(confusion_matrix(all_labels, all_preds))

    # ==========================
    # Save Model
    # ==========================
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    torch.save(model.state_dict(), args.out)
    print(f"\nModel saved to {args.out}")


if __name__ == "__main__":
    main()
