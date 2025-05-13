@echo off
echo ======================================
echo Barbeque Nation Chatbot - Retell API Check
echo ======================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not available
    exit /b 1
)

REM Check if required modules are installed
echo Checking for required Python modules...
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing requests module...
    pip install requests
)

echo.
echo Running Retell API connection test...
echo.
python test_retell_api.py
echo.

if %errorlevel% neq 0 (
    echo ERROR: API connection test failed
    echo.
    echo Troubleshooting tips:
    echo 1. Make sure your .env file has a valid RETELL_API_KEY
    echo 2. Make sure your .env file has a valid DEFAULT_AGENT_ID
    echo 3. Check your internet connection
    echo 4. Verify API key on Retell dashboard: https://app.retellai.com/
) else (
    echo API connection test completed
)

echo.
echo ======================================
pause 