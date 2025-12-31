FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY backend/ ./backend/
COPY app.py ./
COPY .env* ./

# Copy the textbook content (docs folder) - essential for personalization and translation
COPY docs/ ./docs/

# Install any additional dependencies needed
RUN pip install --no-cache-dir sentence-transformers torch

# Expose port (Hugging Face typically uses the PORT environment variable)
EXPOSE 8000

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Starting server..."\n\
echo "Available environment variables:"\n\
env | grep -E "(PORT|GROQ|QDRANT|DATABASE)" || true\n\
export BACKEND_HOST="0.0.0.0"\n\
export BACKEND_PORT="${PORT:-8000}"\n\
echo "Starting server on port $BACKEND_PORT"\n\
cd /app\n\
python app.py' > start.sh && chmod +x start.sh

# Start the application
CMD ["./start.sh"]