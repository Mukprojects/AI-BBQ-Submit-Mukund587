@echo off
echo Barbeque Nation Chatbot Setup
echo ==============================

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.8+ and try again.
    exit /b 1
)

REM Check for Go
go version >nul 2>&1
if %errorlevel% neq 0 (
    echo Go is not installed. Please install Go 1.16+ and try again.
    exit /b 1
)

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Install Go dependencies
echo Installing Go dependencies...
go mod download

echo.
echo Setup complete! To run the application:
echo 1. Ensure you have configured your .env file
echo 2. Run the application with: python server.py
echo 3. In a separate terminal, run: cd chatbot ^& go run server.go
echo.
echo Or run both services with the run.bat script
echo.
pause 