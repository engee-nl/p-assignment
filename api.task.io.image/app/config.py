# app/config.py
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FILENAME = os.path.join(os.path.dirname(__file__), '../logs/app.log')  # Root level

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        RotatingFileHandler(LOG_FILENAME, maxBytes=10000000, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)