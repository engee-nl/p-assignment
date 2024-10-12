from pydantic import BaseModel
from typing import Optional

class ImageDeleteResponse(BaseModel):
    message: str

class UpdateImageDimensions(BaseModel):
    width: int
    height: int