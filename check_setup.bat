@echo off
echo ======================================
echo Barbeque Nation Chatbot - Configuration Check
echo ======================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not available
    echo Please install Python 3.8 or later from https://www.python.org/
    exit /b 1
)

REM Check if required modules are installed
echo Checking for required Python modules...
python -c "import dotenv" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing python-dotenv module...
    pip install python-dotenv
)

python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing requests module...
    pip install requests
)

echo.
echo Running configuration check...
echo.
python check_config.py
echo.

echo ======================================
pause 