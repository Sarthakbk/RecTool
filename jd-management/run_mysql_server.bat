@echo off
echo 🚀 Starting MySQL-based JD Management Server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "mysql_server.py" (
    echo ❌ mysql_server.py not found in current directory
    echo Please run this script from the jd-management directory
    pause
    exit /b 1
)

echo ✅ Python found
echo 📦 Starting MySQL server...
echo.
echo 🌐 Server will be available at:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:5000
echo    Health:   http://localhost:5000/health
echo.
echo 🗄️  Database: MySQL
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the MySQL server
python mysql_server.py

pause
