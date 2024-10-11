# app/main.py
import os
from fastapi import FastAPI
from app.controllers import image_controller, local_image_controller
from app.models.database import init_db
from app.config import logger  # Import logger
from dotenv import load_dotenv  # Import to load environment variables

# Load environment variables from .env file
load_dotenv()

# Get the port from environment variables, default to 8000 if not set
port = int(os.getenv("FASTAPI_PORT", 8000))

app = FastAPI()

# Initialize logging
logger.info("Starting FastAPI application...")

# Initialize the database
@app.on_event("startup")
def on_startup():
    init_db()

# AWS S3 upload controller
app.include_router(image_controller.router)

# Local disk storage controller
app.include_router(local_image_controller.router)

# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)  # Use the port from the config