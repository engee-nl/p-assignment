from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.local_image_service import process_and_save_image, get_all_images, update_image, delete_image, get_image
from app.models.image_schema import ImageDeleteResponse, UpdateImageDimensions

router = APIRouter()

@router.post("/image/upload")
async def upload_image(file: UploadFile = File(...)):
    # Await the process_and_save_image function since it's an async function
    result = await process_and_save_image(file)
    return result

@router.get("/image/list")
def get_images():
    return get_all_images()

@router.put("/image/resize/{md5}")
def update_existing_image(md5: str, update_data: UpdateImageDimensions) -> ImageDeleteResponse:
    try:
        updated = update_image(md5, update_data.width, update_data.height)
        if updated:
            return ImageDeleteResponse(message="Image updated successfully")
        else:
            raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/image/delete/{md5}/", response_model=ImageDeleteResponse)
def delete_existing_image(md5: str) -> ImageDeleteResponse:
    try:
        deleted = delete_image(md5)
        if deleted:
            return ImageDeleteResponse(message="Image deleted successfully")
        else:
            raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/image/get/compressed/{md5}")
async def get_image_from_server(md5: str):
    result = await get_image(md5, "")
    return FileResponse(result)


@router.get("/image/get/original/{md5}")
async def get_original_image_from_server(md5: str):
    result = await get_image(md5, "original")
    return FileResponse(result)