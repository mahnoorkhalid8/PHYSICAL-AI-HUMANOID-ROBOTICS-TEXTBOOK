import logging
import sys
import os
from pathlib import Path

# Add the backend/src directory to the Python path
src_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(src_dir))

from config import settings

def setup_logging():
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create console handler and set level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger

# Set up logging when module is imported
logger = setup_logging()