@echo off
REM Setup batch file for Physical AI Humanoid Robotics Textbook project

echo Physical AI Humanoid Robotics Textbook - Windows Setup
echo =====================================================

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11+ first.
    exit /b 1
)

echo ✅ Node.js and Python are installed

REM Install frontend dependencies
echo Installing frontend dependencies...
npm install

REM Check if backend directory exists
if exist "backend" (
    echo Installing backend dependencies...
    cd backend
    pip install -r requirements.txt
    cd ..
) else (
    echo ⚠️  Backend directory not found. Please ensure the backend exists.
)

REM Check if .env.local exists
if not exist ".env.local" (
    echo ⚠️  .env.local file not found. Please create one based on the documentation.
)

echo Setup completed! 🎉
echo.
echo To start the project:
echo 1. Start the backend: cd backend ^&^& uvicorn src.main:app --reload
echo 2. Start the frontend: npm run start (or npm run dev)
echo.
echo For development, you may need to start Qdrant and Postgres as well.