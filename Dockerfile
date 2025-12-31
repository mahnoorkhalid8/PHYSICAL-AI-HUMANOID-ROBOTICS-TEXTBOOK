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
COPY startup.py ./
COPY .env* ./

# Copy the textbook content (docs folder) - essential for personalization and translation
COPY docs/ ./docs/

# Install any additional dependencies needed
RUN pip install --no-cache-dir sentence-transformers torch

# Expose port (Hugging Face typically uses the PORT environment variable)
EXPOSE 8000

# Create the startup script directly in the container
RUN echo '#!/bin/bash' > start.sh && \
    echo 'set -e  # Exit on any error' >> start.sh && \
    echo '' >> start.sh && \
    echo 'echo "Starting initialization..."' >> start.sh && \
    echo 'echo "Environment variables available:"' >> start.sh && \
    echo 'env | grep -E "PORT|GROQ|QDRANT|DATABASE|HF" || true' >> start.sh && \
    echo '' >> start.sh && \
    echo '# Set default host and port' >> start.sh && \
    echo 'export BACKEND_HOST="0.0.0.0"' >> start.sh && \
    echo 'export BACKEND_PORT="${PORT:-8000}"' >> start.sh && \
    echo '' >> start.sh && \
    echo 'echo "Running startup initialization..."' >> start.sh && \
    echo 'cd /app' >> start.sh && \
    echo 'python startup.py' >> start.sh && \
    echo 'echo "Initialization completed, starting main application..."' >> start.sh && \
    echo 'python app.py' >> start.sh

# Make the script executable
RUN chmod +x start.sh

# Start the application
CMD ["./start.sh"]