@echo off
REM Development start batch file for Physical AI Humanoid Robotics Textbook project

echo Physical AI Humanoid Robotics Textbook - Windows Development Start
echo ================================================================

REM Check if backend directory exists
if not exist "backend" (
    echo ❌ Backend directory not found!
    exit /b 1
)

REM Check if package.json exists
if not exist "package.json" (
    echo ❌ package.json not found! Are you in the correct directory?
    exit /b 1
)

REM Start backend in a separate command window
echo Starting backend server...
start cmd /k "cd backend && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a separate command window
echo Starting frontend server...
start cmd /k "npm run start"

echo Both servers started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000 (or as configured)
echo.
echo Separate command windows have been opened for both servers.
echo You can close them individually when you want to stop the servers.