#!/bin/bash
# Setup script for Physical AI Humanoid Robotics Textbook project

echo "Physical AI Humanoid Robotics Textbook - Setup Script"
echo "====================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.11+ first."
    exit 1
fi

echo "✅ Node.js and Python are installed"

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install

# Check if backend directory exists
if [ -d "backend" ]; then
    echo "Installing backend dependencies..."
    cd backend
    pip install -r requirements.txt
    cd ..
else
    echo "⚠️  Backend directory not found. Please ensure the backend exists."
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚠️  .env.local file not found. Please create one based on the example in the documentation."
fi

echo "Setup completed! 🎉"
echo ""
echo "To start the project:"
echo "1. Start the backend: cd backend && uvicorn src.main:app --reload"
echo "2. Start the frontend: npm run start (or npm run dev)"
echo ""
echo "For development, you may need to start Qdrant and Postgres as well."