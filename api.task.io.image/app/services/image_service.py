# app/services/image_service.py
import hashlib
from PIL import Image
from io import BytesIO
from app.models.database import SessionLocal, Image as ImageModel
from app.utils.s3_utils import upload_file_to_s3
from app.config import logger

def calculate_md5(file):
    """Calculate the MD5 hash of the uploaded file content."""
    md5 = hashlib.md5()
    file.seek(0)  # Ensure we're reading from the start of the file
    while chunk := file.read(8192):
        md5.update(chunk)
    file.seek(0)  # Reset the file pointer after reading
    return md5.hexdigest()

def resize_image(file, size=(200, 200)):
    try:
        image = Image.open(file)
        image = image.resize(size)
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        return buffer
    except Exception as e:
        logger.error(f"Error resizing image: {e}")
        raise

def save_image_to_db(image_id, filename, url):
    db = SessionLocal()
    try:
        image_record = ImageModel(id=image_id, filename=filename, url=url)
        db.add(image_record)
        db.commit()
        db.refresh(image_record)
    except Exception as e:
        logger.error(f"Error saving image to database: {e}")
        raise
    finally:
        db.close()

def process_and_upload_image(file):
    try:
        # Generate MD5 hash from the image content
        image_id = calculate_md5(file.file)

        # Resize the image
        resized_image = resize_image(file.file)

        # Upload to S3
        filename = f"{image_id}.jpg"
        s3_url = upload_file_to_s3(resized_image, filename)

        # Save to the database
        save_image_to_db(image_id, filename, s3_url)

        return {"id": image_id, "filename": filename, "url": s3_url}
    except Exception as e:
        logger.error(f"Error processing and uploading image: {e}")
        raise