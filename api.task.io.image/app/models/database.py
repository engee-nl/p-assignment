# app/models/database.py
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import logger
import os

# Fetch DATABASE_URL from environment, fallback to SQLite for local testing
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://myuser:mypassword@localhost:3306/mydatabase")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Image model with MD5 as the primary key
class Image(Base):
    __tablename__ = "images"

    id = Column(String(32), primary_key=True, index=True)  # MD5 hash as the primary key
    filename = Column(String(255), index=True)
    url = Column(String(255))

# Initialize the database
def init_db():
    '''
    Base.metadata.create_all(bind=engine)
    '''
    logger.info(f"to do : connect to DB")
