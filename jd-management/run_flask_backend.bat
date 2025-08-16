@echo off
echo Starting Flask Backend Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found! Starting Flask backend...
echo.

REM Navigate to backend directory
cd backend

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting Flask server on http://localhost:5000
echo Health check: http://localhost:5000/health
echo API docs: http://localhost:5000/
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
