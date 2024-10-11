# app/controllers/local_image_controller.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.local_image_service import process_and_save_image_locally

router = APIRouter()

@router.post("/upload/local/")
async def upload_image_locally(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    result = process_and_save_image_locally(file)
    return result