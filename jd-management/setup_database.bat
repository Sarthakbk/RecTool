@echo off
echo ========================================
echo    SETTING UP MYSQL DATABASE
echo ========================================
echo.
echo This script will create the database and tables for your Job Description system.
echo.
echo Prerequisites:
echo - MySQL must be installed and running
echo - You need to know your MySQL root password
echo.
echo ========================================
echo.

REM Check if MySQL is accessible
echo Testing MySQL connection...
mysql --version >nul 2>&1
if errorlevel 1 (
    echo ❌ MySQL command not found!
    echo Please make sure MySQL is installed and in your PATH
    echo.
    pause
    exit /b 1
)

echo ✅ MySQL found!
echo.

echo Please enter your MySQL root password when prompted.
echo.
echo Creating database and tables...
echo.

REM Run the SQL script
mysql -u root -p -e "source database/create_job_descriptions_table.sql"

if errorlevel 1 (
    echo.
    echo ❌ Database setup failed!
    echo Please check:
    echo - MySQL is running
    echo - Password is correct
    echo - You have permission to create databases
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Database setup completed successfully!
echo.
echo Created:
echo - Database: rectool_db
echo - Table: job_descriptions
echo - Sample data: 3 job descriptions
echo.
echo You can now start your Flask backend!
echo.
pause
