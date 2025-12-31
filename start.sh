#!/bin/bash
set -e  # Exit on any error

echo "Starting initialization..."
echo "Environment variables available:"
env | grep -E "PORT|GROQ|QDRANT|DATABASE|HF" || true

# Set default host and port
export BACKEND_HOST="0.0.0.0"
export BACKEND_PORT="${PORT:-8000}"

echo "Running startup initialization..."
cd /app
python startup.py
echo "Initialization completed, starting main application..."
python app.py