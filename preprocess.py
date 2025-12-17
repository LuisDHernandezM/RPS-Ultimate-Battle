# Wrote by Luis D. Hernandez with assistance from ChatGPT and GenAI
# Date: December 2025
# This file is for processing the drawings and cleaning it up
# # It uses OpenCV to preprocess the image for model prediction


# preprocess.py
import cv2  # type: ignore
import numpy as np
import os

DEBUG_DIR = "debug_preproc"
os.makedirs(DEBUG_DIR, exist_ok=True)

def _uint8_for_debug(img_float):
    """Convert a float image in [0,1] or a uint8 image to uint8 for saving."""
    if img_float is None:
        return None
    if img_float.dtype == np.float32 or img_float.dtype == np.float64:
        tmp = (np.clip(img_float, 0.0, 1.0) * 255.0).astype(np.uint8)
        return tmp
    return img_float.astype(np.uint8)

def preprocess_image(path, size=64, save_debug=True):
    """
    Load image from path and return a (size, size, 1) float32 numpy array (0..1).
    Produces debug images (raw, threshold, crop, final) in debug_preproc/ when save_debug=True.
    This function is safe if there's no drawing (returns blank image).
    """
    # 1) Raw (color) image - used only for debug saving
    raw_bgr = cv2.imread(path, cv2.IMREAD_COLOR)  # BGR as loaded by OpenCV
    if raw_bgr is None:
        # if file missing, return blank
        blank = np.zeros((size, size, 1), dtype=np.float32)
        if save_debug:
            cv2.imwrite(f"{DEBUG_DIR}/debug_raw_missing.png", np.zeros((size, size, 3), dtype=np.uint8))
        return blank

    # Save raw debug
    if save_debug:
        try:
            cv2.imwrite(f"{DEBUG_DIR}/debug_raw.png", raw_bgr)
        except Exception:
            pass

    # 2) Convert to grayscale for shape processing
    gray = cv2.cvtColor(raw_bgr, cv2.COLOR_BGR2GRAY)

    # 3) Adaptive threshold (more robust to light/dark strokes)
    try:
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            15, 3
        )
    except Exception:
        # Fallback to simple threshold if adaptive fails
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    if save_debug:
        cv2.imwrite(f"{DEBUG_DIR}/debug_thresh.png", thresh)

    # 4) Find non-zero pixels (the drawing)
    coords = cv2.findNonZero(thresh)
    if coords is None:
        # No drawing found -> return blank (but still save debug)
        blank_uint8 = np.zeros((size, size, 3), dtype=np.uint8)
        if save_debug:
            cv2.imwrite(f"{DEBUG_DIR}/debug_no_drawing.png", blank_uint8)
        return np.zeros((size, size, 1), dtype=np.float32)

    # 5) Bounding box + crop (safe)
    x, y, w, h = cv2.boundingRect(coords)
    # add a small padding so thin strokes are not cropped out entirely
    pad = max(2, int(0.05 * max(w, h)))
    x0 = max(0, x - pad)
    y0 = max(0, y - pad)
    x1 = min(gray.shape[1], x + w + pad)
    y1 = min(gray.shape[0], y + h + pad)
    cropped = thresh[y0:y1, x0:x1]

    # Save the crop debug (converted to uint8)
    if save_debug:
        cv2.imwrite(f"{DEBUG_DIR}/debug_crop.png", _uint8_for_debug(cropped))

    # 6) Resize to (size, size)
    final = cv2.resize(cropped, (size, size), interpolation=cv2.INTER_AREA)

    # 7) Normalize to 0..1 and add channel
    final_float = (final.astype(np.float32) / 255.0).reshape(size, size, 1)

    # 8) Save final debug image (uint8 visualization)
    if save_debug:
        cv2.imwrite(f"{DEBUG_DIR}/debug_final64.png", _uint8_for_debug(final))

    return final_float