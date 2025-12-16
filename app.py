# Hugging Face Space app.py for the Physical AI Humanoid Robotics Textbook Chatbot
import os
from backend.src.main import app

# This file allows the application to be run on Hugging Face Spaces
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))