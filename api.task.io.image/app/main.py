# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.controllers import image_controller, local_image_controller
from app.models.database import init_db
from app.config import logger  # Import logger
from dotenv import load_dotenv  # Import to load environment variables
import traceback

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

@app.middleware("http")
async def log_exceptions_middleware(request: Request, call_next):
    try:
        # Proceed with the request
        response = await call_next(request)
        return response
    except Exception as exc:
        # Log error with traceback
        error_trace = traceback.format_exc()  # Capture stack trace
        logger.error(f"Request failed: {request.method} {request.url}")
        logger.error(f"Traceback: {error_trace}")

        # Return custom error response
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error. Please check the logs for more details."},
        )

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