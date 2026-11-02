import streamlit as st
import torch
import torch.nn as nn

import torchvision.models as models
import torchvision.transforms as transforms

from PIL import Image


from fastapi import FastAPI, UploadFile, File, HTTPException #for error handling

import json
import os
from pathlib import Path





#basic settings

APP_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(APP_PATH, "data")

MODELS_PATH = os.path.join(APP_PATH, "models")

MODEL_PATH = os.path.join(MODELS_PATH, "resnet18_final.pth")

CLASS_PATH = os.path.join(MODELS_PATH, "class_names.json")


API_URL = "http://127.0.0.1:8000/"

base_url = os.getcwd()

LOGO_URL = os.path.join(base_url, "logo.png")


# Page configuration

st.set_page_config(
    page_title="Facial Emotion Recognition",
    page_icon="😊",
    layout="wide"
)


# Application heading

st.title("Facial Emotion Recognition System")

st.write(
    "Upload a facial image and let our trained "
    "ResNet18 model predict the emotion."
)

st.divider()
