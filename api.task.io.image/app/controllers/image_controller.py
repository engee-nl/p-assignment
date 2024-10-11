# app/controllers/image_controller.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.image_service import process_and_upload_image

router = APIRouter()

@router.post("/upload/s3/")
async def upload_image_to_s3(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    result = process_and_upload_image(file)
    return result