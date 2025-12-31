from backend.src.main import app
import uvicorn
import os
from threading import Thread

# For Hugging Face Spaces, we need to run the FastAPI app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)