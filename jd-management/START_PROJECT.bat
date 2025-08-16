@echo off
echo ========================================
echo    JOB DESCRIPTION MANAGEMENT SYSTEM
echo ========================================
echo.
echo This script will help you start your complete project
echo.
echo Prerequisites:
echo - Python 3.8+ installed
echo - Node.js 16+ installed  
echo - MySQL 8.0+ installed and running
echo - MySQL database setup completed
echo.
echo ========================================
echo.

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    echo Download from: https://python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python found!

REM Check Node.js
echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found! Please install Node.js first.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js found!

echo.
echo ========================================
echo CHOOSE YOUR STARTUP OPTION:
echo ========================================
echo.
echo 1. Start Backend Only (Flask + MySQL)
echo 2. Start Frontend Only (React)
echo 3. Start Both Backend and Frontend
echo 4. Setup Database First
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto :backend
if "%choice%"=="2" goto :frontend  
if "%choice%"=="3" goto :both
if "%choice%"=="4" goto :database
if "%choice%"=="5" goto :exit
goto :invalid

:backend
echo.
echo Starting Backend Only...
echo.
echo Make sure you have:
echo - MySQL running
echo - Database 'rectool_db' created
echo - Table 'job_descriptions' created
echo.
echo Starting Flask backend...
start "Flask Backend" cmd /k "run_flask_backend.bat"
echo ✅ Backend started in new window!
echo Backend will be available at: http://localhost:5000
pause
goto :menu

:frontend
echo.
echo Starting Frontend Only...
echo.
echo Note: Frontend needs backend to be running for full functionality
echo.
echo Starting React frontend...
start "React Frontend" cmd /k "run_frontend.bat"
echo ✅ Frontend started in new window!
echo Frontend will be available at: http://localhost:3000
pause
goto :menu

:both
echo.
echo Starting Both Backend and Frontend...
echo.
echo Starting Flask backend...
start "Flask Backend" cmd /k "run_flask_backend.bat"
timeout /t 3 /nobreak >nul
echo Starting React frontend...
start "React Frontend" cmd /k "run_frontend.bat"
echo.
echo ✅ Both services started!
echo.
echo Access Points:
echo - Backend API: http://localhost:5000
echo - Frontend App: http://localhost:3000
echo - Health Check: http://localhost:5000/health
echo - API Docs: http://localhost:5000/
echo.
pause
goto :menu

:database
echo.
echo ========================================
echo DATABASE SETUP INSTRUCTIONS
echo ========================================
echo.
echo 1. Open MySQL Workbench or MySQL command line
echo 2. Connect to your MySQL server as root
echo 3. Run the SQL script: database/create_job_descriptions_table.sql
echo.
echo OR use command line:
echo mysql -u root -p ^< database/create_job_descriptions_table.sql
echo.
echo This will create:
echo - Database: rectool_db
echo - Table: job_descriptions
echo - Sample data: 3 job descriptions
echo.
echo After database setup, come back and choose option 3
echo.
pause
goto :menu

:invalid
echo.
echo ❌ Invalid choice! Please enter 1-5
pause
goto :menu

:menu
echo.
echo ========================================
echo MAIN MENU
echo ========================================
echo.
echo 1. Start Backend Only (Flask + MySQL)
echo 2. Start Frontend Only (React)
echo 3. Start Both Backend and Frontend
echo 4. Setup Database First
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto :backend
if "%choice%"=="2" goto :frontend  
if "%choice%"=="3" goto :both
if "%choice%"=="4" goto :database
if "%choice%"=="5" goto :exit
goto :invalid

:exit
echo.
echo Goodbye! 👋
echo.
pause
exit /b 0
