# This file is for processing the drawings and cleaning it up
# # It uses OpenCV to preprocess the image for model prediction
# Helper file for AI, not important for main logic

import cv2 # type: ignore
import numpy as np

def preprocess_image(path):
    # Load image in grayscale
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Threshold to get binary image
    _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

    # Find bounding box of the drawing
    coords = cv2.findNonZero(img)
    x, y, w, h = cv2.boundingRect(coords)

    # Crop to the drawing
    img = img[y:y+h, x:x+w]

    # Resize to 64x64
    img = cv2.resize(img, (64, 64))

    # Normalize to 0–1
    img = img / 255.0

    # Add channel dimension for CNN
    img = img.reshape(64, 64, 1)

    return img