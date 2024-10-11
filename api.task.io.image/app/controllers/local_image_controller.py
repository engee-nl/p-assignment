from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.local_image_service import process_and_save_image, get_all_images, update_image, delete_image, get_image
from app.models import ImageDeleteResponse

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

@router.delete("/delete/{md5}/", response_model=ImageDeleteResponse)
def delete_existing_image(md5: str) -> ImageDeleteResponse:
    try:
        deleted = delete_image(md5)
        if deleted:
            return ImageDeleteResponse(message="Image deleted successfully")
        else:
            raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/image/compressed/{md5}")
async def get_image_from_server(md5: str):
    result = await get_image(md5)
    return FileResponse(result)