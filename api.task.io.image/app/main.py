# app/main.py
from fastapi import FastAPI
from app.controllers import image_controller, local_image_controller
from app.models.database import init_db

app = FastAPI()

# Initialize the database
@app.on_event("startup")
def on_startup():
    init_db()

# AWS S3 upload controller
app.include_router(image_controller.router)

# Local disk storage controller
app.include_router(local_image_controller.router)

# Run with: uvicorn app.main:app --reload