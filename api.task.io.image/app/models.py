from pydantic import BaseModel
from typing import Optional

class ImageUploadResponse(BaseModel):
    message: str
    image_id: Optional[str] = None
    url: Optional[str] = None

class ImageUpdateResponse(BaseModel):
    message: str
    image_id: str
    url: str

class ImageDeleteResponse(BaseModel):
    message: str

class ImageModel(BaseModel):
    image_id: str
    filename: str
    url: str