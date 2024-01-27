from fastapi import Request
import logging
from dotenv import load_dotenv
import os

debug_mode = os.getenv("DEBUG")

logger = logging.getLogger("custom_logger")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("app_log.log")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

async def custom_logging(request: Request, call_next):
    # Logs the request information before handling it
    logger.debug(f"Request received: {request.method} - {request.url}")
    response = await call_next(request)
    # Log the response information after handling the request
    logger.debug(f"Response status: {response.status_code}")
    return response
