
# Mosaic Match – AI Arena
Human vs AI image matching game using pretrained ResNet18 and computer vision

A gamified computer vision project that compares human image matching with AI-based image matching.

## Features
- Distorted target image generation using image augmentation.
- Human vs AI matching challenge.
- Pretrained ResNet18 for feature extraction.
- Cosine similarity for selecting the closest matching image.
- Streamlit interface with scores and performance statistics.

## Technologies
- Python
- PyTorch and Torchvision
- NumPy and Pillow
- Streamlit

## Dataset
A selected subset of images from the [Similix Image Dataset on Kaggle](https://www.kaggle.com/datasets/ashishpatel8736/similix-image-dataset/data) is used for the matching game.

## Run locally

1. Clone or download this repository.
2. Install dependencies:

   `pip install -r requirements.txt`

3. Ensure the selected images are in the `images/` folder.
4. Start the application:

   `streamlit run app.py`

The application runs locally in your browser.

## Methodology
The game generates a distorted target from one of the selected images. A pretrained ResNet18 model extracts feature embeddings from the target and candidate images. Cosine similarity is used to rank the candidates, and the highest-scoring candidate is selected as the AI's prediction.

The model uses pretrained weights and is not fine-tuned on the project dataset.

