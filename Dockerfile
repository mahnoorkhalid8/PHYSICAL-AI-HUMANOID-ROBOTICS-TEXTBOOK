FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code
COPY backend/src/ ./backend/src/
COPY backend/.env ./backend/

# Install any additional dependencies needed
RUN pip install --no-cache-dir sentence-transformers torch

# Expose port
EXPOSE 8000

# Start the backend server
CMD ["uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "8000"]