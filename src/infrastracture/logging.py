import sys
from loguru import logger
from src.config import settings
logger.remove()  # remove the default python logging handler

def setup_logging():
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG",
    )
    logger.info(f"Logging Initialized for {settings.PROJECT_NAME}")