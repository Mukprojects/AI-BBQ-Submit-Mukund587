@echo off
echo Starting Barbeque Nation Chatbot...
echo.

rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python 3.8 or newer and try again.
    goto :end
)

rem Check if required packages are installed
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
)

echo Starting the Python API server on port 8000...
start cmd /k python server.py

echo Starting the Go web server on port 8080...
cd chatbot
echo Please visit http://localhost:8080/ to access the chatbot.
go run server.go

:end
pause 