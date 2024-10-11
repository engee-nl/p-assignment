# app/utils/file_utils.py
import os
from pathlib import Path

IMAGE_DIR = Path("uploaded_images")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

def save_image_to_disk(image_data, filename):
    file_path = IMAGE_DIR / filename
    with open(file_path, "wb") as f:
        f.write(image_data.getbuffer())
    return str(file_path)