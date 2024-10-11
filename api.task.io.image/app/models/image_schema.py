from pydantic import BaseModel
from typing import Optional

class ImageDeleteResponse(BaseModel):
    message: str