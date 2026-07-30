
import argparse

import torch
from PIL import Image

from src.model import CatDogCNN, inference_transform, CLASS_NAMES


def load_model(weights_path="models/cat_dog_cnn.pth", device="cpu"):
    model = CatDogCNN()
    state_dict = torch.load(weights_path, map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model


def predict_image(image, model, transform=inference_transform, class_names=CLASS_NAMES):
    """
    image : file path (str) OR a PIL.Image (so the Streamlit app can pass
            an uploaded file straight in without saving it to disk first)
    """

    if isinstance(image, str):
        image = Image.open(image)

    image = image.convert("RGB")
    image_tensor = transform(image).unsqueeze(0)  # add batch dimension

    with torch.no_grad():
        output = model(image_tensor)
        probs = torch.softmax(output, dim=1)[0]
        pred_idx = torch.argmax(probs).item()

    return class_names[pred_idx], probs[pred_idx].item(), probs.tolist()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict Cat / Dog on a single image")
    parser.add_argument("image_path", help="path to the image file")
    parser.add_argument("--weights", default="models/cat_dog_cnn.pth")
    args = parser.parse_args()

    model = load_model(args.weights)
    label, confidence, _ = predict_image(args.image_path, model)

    print(f"Prediction: {label}  ({confidence*100:.2f}% confidence)")
