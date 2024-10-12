# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import image_controller, local_image_controller
from app.models.database import init_db
from app.config import logger 
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Define the list of allowed origins
allowed_origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000",
    "http://ec2-43-201-64-153.ap-northeast-2.compute.amazonaws.com:3000",
]

# Add CORSMiddleware to allow the defined origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Allows requests from specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
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