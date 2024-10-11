import os
import hashlib
from PIL import Image
from fastapi import UploadFile, HTTPException
import json
from typing import List

UPLOAD_FOLDER = "uploaded_images"
JSON_FILE = "image_list.json"
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

def save_image_list_to_json(image_list: List[dict]):
    with open(JSON_FILE, 'w') as f:
        json.dump(image_list, f, indent=4)

def load_image_list_from_json() -> List[dict]:
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, 'r') as f:
            content = f.read().strip()  # Strip any extra whitespace or newlines
            if not content:  # If file is empty, return an empty list
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        # If the file is not valid JSON, return an empty list
        return []

def calculate_md5(file: UploadFile) -> str:
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file.file.read(4096), b""):
        hash_md5.update(chunk)
    file.file.seek(0)  # Reset file pointer after reading
    return hash_md5.hexdigest()

def save_original_image(file: UploadFile, md5_hash: str) -> str:
    ext = file.filename.split('.')[-1]
    original_filename = f"{md5_hash}.{ext}"
    original_path = os.path.join(UPLOAD_FOLDER, original_filename)
    with open(original_path, "wb") as f:
        f.write(file.file.read())
    file.file.seek(0)  # Reset file pointer after saving
    return original_path

def compress_image_to_jpg(original_path: str, md5_hash: str) -> str:
    img = Image.open(original_path)
    jpg_filename = f"{md5_hash}.jpg"
    jpg_path = os.path.join(UPLOAD_FOLDER, jpg_filename)
    img = img.convert("RGB")  # Convert to RGB if it's not already
    img.save(jpg_path, "JPEG", quality=70)
    return jpg_path

def process_and_save_image(file: UploadFile):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File size exceeds 20MB")

    md5_hash = calculate_md5(file)
    
    image_list = load_image_list_from_json()

    # Check if image already exists
    if any(img['md5'] == md5_hash for img in image_list):
        raise HTTPException(status_code=400, detail="Image already exists")
    
    # Save original image
    original_path = save_original_image(file, md5_hash)

    # Compress the image to JPG
    compressed_image_path = compress_image_to_jpg(original_path, md5_hash)

    # Save image info to JSON
    image_list.append({"filename": file.filename, "md5": md5_hash, "original_path": original_path, "compressed_path": compressed_image_path})
    save_image_list_to_json(image_list)

    return {"md5": md5_hash, "compressed_image": compressed_image_path}

def get_all_images() -> List[dict]:
    image_list = load_image_list_from_json()
    return image_list

def update_image(md5: str, new_width: int, new_height: int):
    image_list = load_image_list_from_json()
    image_data = next((img for img in image_list if img['md5'] == md5), None)
    
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")
    
    original_path = image_data["original_path"]
    
    # Resize the image
    img = Image.open(original_path)
    img = img.resize((new_width, new_height))
    resized_image_path = f"{os.path.splitext(original_path)[0]}_{new_width}x{new_height}.jpg"
    img.save(resized_image_path, "JPEG", quality=70)

    return {"resized_image": resized_image_path}

def delete_image(md5: str):
    image_list = load_image_list_from_json()
    image_data = next((img for img in image_list if img['md5'] == md5), None)
    
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")
    
    original_path = image_data["original_path"]
    compressed_path = image_data["compressed_path"]
    
    # Remove files from disk
    if os.path.exists(original_path):
        os.remove(original_path)
    if os.path.exists(compressed_path):
        os.remove(compressed_path)
    
    # Remove from JSON
    image_list = [img for img in image_list if img['md5'] != md5]
    save_image_list_to_json(image_list)

    return {"message": "Image deleted successfully"}