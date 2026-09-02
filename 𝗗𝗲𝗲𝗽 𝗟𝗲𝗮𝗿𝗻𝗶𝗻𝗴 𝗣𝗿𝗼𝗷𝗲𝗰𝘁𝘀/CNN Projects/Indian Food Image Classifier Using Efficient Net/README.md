# Indian Food Image Classifier

AI-powered Indian food recognition built on **EfficientNet-B0** transfer learning,
served through a professional Streamlit interface.

---

## Overview

This project classifies photographs of Indian dishes into five food categories.
A pretrained EfficientNet-B0 backbone (ImageNet weights) was frozen and its
classification head replaced with a 5-way linear layer, then fine-tuned on a
curated Indian food dataset. The trained weights are shipped in `models/`, and
`app.py` loads them for inference — no training, no dataset download, and no
Kaggle credentials are needed to run the application.

## Features

- AI-based Indian food image classification
- EfficientNet-B0 backbone with a fine-tuned 5-class head
- **One-click sample gallery** — try the classifier instantly without finding an image
- **Result detail toggle** — switch between the top prediction only and the full class breakdown
- Top-1 prediction with a confidence score
- Full probability distribution across all classes, sorted high → low
- Low-confidence warning for out-of-domain images
- Prediction details panel (model, class count, resolution, device)
- Cached model loading (`@st.cache_resource`) and `torch.no_grad()` inference
- Automatic CUDA detection with full CPU support
- Polished, responsive Streamlit UI with custom CSS

## Supported Classes

| Class label      | Display name   |
| ---------------- | -------------- |
| `biryani`        | Biryani        |
| `butter_chicken` | Butter Chicken |
| `gulab_jamun`    | Gulab Jamun    |
| `naan`           | Naan           |
| `palak_paneer`   | Palak Paneer   |

## Model

- **Architecture:** EfficientNet-B0 (`torchvision.models.efficientnet_b0`)
- **Head:** `classifier[1]` replaced with `nn.Linear(1280, 5)`
- **Artifact used for inference:** `models/efficientnet_b0_best.pth`
  (a plain `state_dict`; `models/efficientnet_b0_final.pth` is the automatic fallback)
- **Class mapping:** `models/class_to_idx.json`, falling back to
  `models/indian_food_class_to_idx.json`

### Inference preprocessing

Identical to the notebook's `eval_transform`:

```python
transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])
```

Uploaded images are EXIF-rotated and converted to RGB before this pipeline runs.

## Performance

```text
Model:            EfficientNet-B0
Test Accuracy:    84.21%
Test Samples:     38
Number of Classes: 5
```

The test set is small (38 samples), so the reported accuracy carries a wide
confidence interval and should be read as indicative rather than definitive.

## Project Structure

```text
Indian Food Image Classifier/
├── app.py                  # Streamlit inference application
├── requirements.txt        # Runtime dependencies
├── README.md
├── .streamlit/
│   └── config.toml         # UI theme and upload limit
├── assets/
│   └── samples/            # bundled one-click demo images (<class>.jpg)
├── data/
│   └── data.md             # Dataset notes (dataset itself is not required)
├── graphs/
│   └── final_visualizing_sample_images.png
├── models/
│   ├── efficientnet_b0_best.pth        # weights used by the app
│   ├── efficientnet_b0_final.pth       # fallback weights
│   ├── efficientnet_metrics.json       # accuracy / sample counts
│   ├── class_to_idx.json               # class mapping (EfficientNet run)
│   ├── indian_food_class_to_idx.json   # class mapping (baseline run)
│   └── indian_food_model_baseline.pth  # earlier custom-CNN baseline
└── notebook/
    └── Indian_Food_Image_Classifier.ipynb   # full training workflow
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

For a smaller CPU-only PyTorch install:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install streamlit Pillow numpy
```

## Run

```bash
streamlit run app.py
```

The app opens at <http://localhost:8501>. Upload a JPG, JPEG, PNG or WEBP image
of a dish to get a prediction.

## Limitations

- The model recognises **only the five trained categories**. It has no "unknown"
  class, so an unrelated image is still forced into the closest known class.
- Predictions below 60% confidence trigger an on-screen warning and should be
  treated as inconclusive.
- Accuracy was measured on 38 test images; real-world performance will vary with
  lighting, plating, camera angle and regional dish variation.
- Images containing multiple dishes are not supported — the model produces a
  single label per image.
