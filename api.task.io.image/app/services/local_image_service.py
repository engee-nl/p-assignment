import os
import hashlib
from app.config import logger  # Import logger
from PIL import Image
from fastapi import UploadFile, HTTPException
import json
import aiofiles
from typing import List
from pathlib import Path
import time

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

async def process_and_save_image(file: UploadFile):
    # Step 1: Save the original file to disk first
    try:
        original_file_location = f"uploaded_images/{file.filename}"
        
        # Save the file asynchronously to avoid blocking the event loop
        async with aiofiles.open(original_file_location, 'wb') as out_file:
            while content := await file.read(1024):  # Read in chunks to handle large files
                await out_file.write(content)

        # Ensure the file is fully written before moving on
        await file.seek(0)  # Reset file pointer after saving

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error saving the original image")

    # Step 2: After the file is fully saved, check its MD5 hash
    try:
        md5_hash = hashlib.md5()
        async with aiofiles.open(original_file_location, 'rb') as f:
            while chunk := await f.read(8192):
                md5_hash.update(chunk)
        file_md5 = md5_hash.hexdigest()

        # Check if the image already exists by MD5
        image_list = load_image_list_from_json()
        if any(image['md5'] == file_md5 for image in image_list):
        #if os.path.exists(f"uploaded_images/{file_md5}.jpg"):
            raise HTTPException(status_code=409, detail="Image already exists")

    except Exception as e:
        logger.error(f"Error calculating MD5 hash: {e}")
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

    # Step 3: Resize and convert the image after saving the original
    try:
        with Image.open(original_file_location) as img:
            original_width, original_height = img.size
        
            # Set desired width and height
            desired_width = 800
            desired_height = None  # Keep None to maintain aspect ratio
            
            if desired_height is None:
                aspect_ratio = original_height / original_width
                desired_height = int(desired_width * aspect_ratio)

            # Resize the image
            resized_image = img.resize((desired_width, desired_height))
            resized_image = resized_image.convert("RGB")  # Convert to JPG

            # Save the resized image with 70% quality
            resized_file_location = f"uploaded_images/{file_md5}.jpg"
            resized_image.save(resized_file_location, "JPEG", quality=70)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resizing or converting the image: {e}")

    # Step 4: Save image info to JSON
    image_url = os.getenv("IMAGE_HOST_URL")
    timestamp = int(time.time())
    
    image_data = {
        "filename": file.filename,
        "md5": file_md5,
        "original_path": original_file_location,
        "compressed_path": resized_file_location,
        "image_url": f"{image_url}/image/get/compressed/{file_md5}?t={timestamp}",
        "original_image_url": f"{image_url}/image/get/original/{file_md5}?t={timestamp}"
    }

    # Append new image info
    image_list.append(image_data)
    save_image_list_to_json(image_list)

    # Return a JSON response with the saved image details
    return {
        "filename": file.filename,
        "md5": file_md5,
        "original_path": original_file_location,
        "compressed_path": resized_file_location,
        "image_url": f"{image_url}/image/get/compressed/{file_md5}?t={timestamp}",
        "original_image_url": f"{image_url}/image/get/original/{file_md5}?t={timestamp}"
    }

def get_all_images() -> List[dict]:
    image_list = load_image_list_from_json()
    return image_list

def update_image(md5: str, new_width: int, new_height: int):
    image_list = load_image_list_from_json()
    image_data = next((img for img in image_list if img['md5'] == md5), None)
    
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")
    
    original_path = image_data["original_path"]
    image_url = os.getenv("IMAGE_HOST_URL")

    # Resize and convert the image after saving the original
    try:
        with Image.open(original_path) as img:
            original_width, original_height = img.size
        
            # Set desired width and height
            desired_width = new_width
            desired_height = None  # Keep None to maintain aspect ratio
            
            if desired_height is None:
                aspect_ratio = original_height / original_width
                desired_height = int(desired_width * aspect_ratio)

            # Resize the image
            resized_image = img.resize((desired_width, desired_height))
            resized_image = resized_image.convert("RGB")  # Convert to JPG

            # Save the resized image with 70% quality
            resized_file_location = f"uploaded_images/{md5}.jpg"
            resized_image.save(resized_file_location, "JPEG", quality=70)

            # Modify the image entry with new dimensions and Update the JSON file
            # Find the image entry with the specified md5
            timestamp = int(time.time())
            for image_entry in image_list:
                if image_entry.get("md5") == md5:
                    image_entry["image_url"] = f"{image_url}/image/get/compressed/{md5}?t={timestamp}"
                    break
            else:
                raise HTTPException(status_code=404, detail="Image not found")
            
            save_image_list_to_json(image_list)

    except Exception as e:
        logger.error(f"Error resizing or converting the image: {e}")
        raise HTTPException(status_code=500, detail=f"Error resizing or converting the image: {e}")

    # Return a JSON response with the saved image details
    return {
        "compressed_path": resized_file_location,
        "image_url": f"{image_url}/image/get/compressed/{md5}"
    }

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

async def get_image(md5key: str, type: str):
    try:
        image_list = load_image_list_from_json()
        image_data = next((image for image in image_list if image['md5'] == md5key), None)
        
        # Check if the image info exists
        if image_data is None:
            logger.error(f"Image not found")
            raise HTTPException(status_code=404, detail="Image not found")

        # Retrieve the file path from the image info
        image_path = image_data['compressed_path']
        if type == "original":
            image_path = image_data['original_path']

        logger.info(f"Image path : {image_path}")

        # Check if the file exists
        if not Path(image_path).exists():
            logger.error(f"Image file not found")
            raise HTTPException(status_code=404, detail="Image file not found")
        
        # Return the file as a response
        return image_path

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))