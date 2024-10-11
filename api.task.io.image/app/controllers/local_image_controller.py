from fastapi import APIRouter, UploadFile, HTTPException, File
from app.services.local_image_service import process_and_save_image, get_all_images, update_image, delete_image

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Await the process_and_save_image function since it's an async function
    result = await process_and_save_image(file)
    return result

@router.get("/images")
def get_images():
    return get_all_images()

@router.put("/update/{md5}")
def update_existing_image(md5: str, width: int, height: int):
    return update_image(md5, width, height)

@router.delete("/delete/{md5}")
def delete_existing_image(md5: str):
    return delete_image(md5)

@router.get("/image/compressed/{md5key}")
def get_image(md5: str):
    return get_image(md5)