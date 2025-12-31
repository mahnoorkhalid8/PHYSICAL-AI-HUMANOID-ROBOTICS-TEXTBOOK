from backend.src.main import app
import uvicorn
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# For Hugging Face Spaces, we need to run the FastAPI app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("BACKEND_HOST", "0.0.0.0")

    logger.info(f"Starting server on {host}:{port}")

    # Small delay to ensure services are ready
    time.sleep(1)

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )