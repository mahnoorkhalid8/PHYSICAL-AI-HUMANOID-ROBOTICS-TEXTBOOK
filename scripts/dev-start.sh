#!/bin/bash
# Development start script for Physical AI Humanoid Robotics Textbook project

echo "Physical AI Humanoid Robotics Textbook - Development Start"
echo "========================================================="

# Function to start backend
start_backend() {
    if [ -d "backend" ]; then
        echo "Starting backend server..."
        cd backend
        uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &
        BACKEND_PID=$!
        cd ..
        echo "Backend started with PID: $BACKEND_PID"
    else
        echo "❌ Backend directory not found!"
        exit 1
    fi
}

# Function to start frontend
start_frontend() {
    echo "Starting frontend server..."
    npm run start &
    FRONTEND_PID=$!
    echo "Frontend started with PID: $FRONTEND_PID"
}

# Check if both backend and frontend exist
if [ ! -d "backend" ]; then
    echo "❌ Backend directory not found!"
    exit 1
fi

if [ ! -f "package.json" ]; then
    echo "❌ package.json not found! Are you in the correct directory?"
    exit 1
fi

# Start backend first
start_backend

# Wait a moment for backend to start
sleep 3

# Start frontend
start_frontend

echo "Both servers started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000 (or as configured)"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "PID Backend: $BACKEND_PID"
echo "PID Frontend: $FRONTEND_PID"

# Wait for user to press Ctrl+C
wait $BACKEND_PID $FRONTEND_PID