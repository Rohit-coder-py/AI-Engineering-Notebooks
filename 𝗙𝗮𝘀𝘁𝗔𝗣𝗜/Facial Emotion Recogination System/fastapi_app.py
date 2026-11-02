import torch
import torch.nn as nn

import torchvision.models as models
import torchvision.transforms as transforms

from PIL import Image


from fastapi import FastAPI, UploadFile, File, HTTPException #for error handling

from pathlib import Path
import json
import os
from pathlib import Path

#basic settings

APP_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(APP_PATH, "data")

MODELS_PATH = os.path.join(APP_PATH, "models")

MODEL_PATH = os.path.join(MODELS_PATH, "resnet18_final.pth")

CLASS_PATH = os.path.join(MODELS_PATH, "class_names.json")





# #load emotion class names

with open(CLASS_PATH, "r") as file:
    class_names = json.load(file)

print("Classes:", class_names)



#basic app confriguaton

# Initialize FastAPI application

app = FastAPI(title="Facial Emotion Recognition API",description="API for predicting facial emotions using ResNet18",)

@app.get("/")
def home():
    return {
        "message": "Facial Emotion Recognition API is running",
        "model": "ResNet18",
        "classes": class_names
    }



#Load the trained ResNet18 model


device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Using device:", device)


#now lets Load trained checkpoint

checkpoint = torch.load(
    MODEL_PATH,
    map_location=device,
    weights_only=True
)

print("done")

#in model inference notebook we got that our model is traied on these values : model_state_dict
# class_names

# image_size

# imagenet_mean

# imagenet_std

# val_accuracy

# test_accuracy


#Extract model configuration

class_names = checkpoint["class_names"]

IMAGE_SIZE = checkpoint["image_size"]

imagenet_mean = checkpoint["imagenet_mean"]

imagenet_std = checkpoint["imagenet_std"]

print("Image Size:", IMAGE_SIZE)
print("Classes:", class_names)


#from main  notebook  recreate ResNet18 architecture

model = models.resnet18(weights=None)

model.fc = nn.Sequential(nn.Dropout(0.4),
                         nn.Linear(model.fc.in_features,len(class_names)))


#weights

model.load_state_dict(
    checkpoint["model_state_dict"])


model = model.to(device)

model.eval()

#now for images we need to transform for resnet

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    
    
    transforms.Normalize(mean=imagenet_mean,std=imagenet_std)])




#now troch work is ended now set endpoint of fastapi
from io import BytesIO #we will use this to process imgs


@app.post("/predict")
async def predict_emotion(file: UploadFile = File(...)):

    #Read uploaded image
    image_bytes = await file.read()

    #Convert 
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    image_tensor = transform(image)

    #batch
    image_tensor = image_tensor.unsqueeze(0)

    
    image_tensor = image_tensor.to(device)

    #model inference part from the notebook
    with torch.inference_mode():

        outputs = model(image_tensor)

        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities,dim=1)

    predicted_class = class_names[predicted.item()]

    confidence_score = confidence.item() * 100
    
    
    #also return probab score of all classes
    
    # Convert all probabilities into a dictionary

    emotion_scores = {
        class_names[i]: round(probabilities[0][i].item() * 100, 2)
        for i in range(len(class_names))
    }

    return {
        "filename": file.filename,
        "predicted_emotion": predicted_class,
        "confidence": round(confidence_score, 2),
        "emotion_scores": emotion_scores
    }
        
    
#/health

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model": "ResNet18",
        "model_loaded": model is not None,
        "device": str(device)
    }


#completed 