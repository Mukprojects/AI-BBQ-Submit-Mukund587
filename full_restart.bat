@echo off
echo ======================================
echo Barbeque Nation Chatbot - Full Restart
echo ======================================

echo Stopping all existing servers...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM go.exe >nul 2>&1

echo.
echo Copying .env to chatbot directory...
copy /Y .env chatbot\.env >nul 2>&1

REM Load the phone number from .env
for /f "tokens=*" %%a in ('type .env ^| findstr "TWILIO_PHONE_NUMBER"') do (
    set %%a
)

if "%TWILIO_PHONE_NUMBER%"=="" (
    set TWILIO_PHONE_NUMBER=+19787185545
)

echo.
echo Running API connection test...
call check_retell_api.bat

echo.
echo Starting servers with fresh state...
start cmd /k "title BBQ Nation Python Server && python server.py"

echo.
echo Waiting 5 seconds for Python server to initialize...
timeout /t 5 /nobreak >nul

echo.
echo Starting Go server (port 8080)...
start cmd /k "title BBQ Nation Go Server && cd chatbot && go run server.go"

echo.
echo Both servers starting...
echo.
echo URLs:
echo - Knowledge Base API: http://localhost:8000/kb/docs
echo - Webhook API: http://localhost:8000/webhook
echo - Web Chatbot: http://localhost:8080/
echo - API Debug: http://localhost:8080/api/debug
echo.
echo Voice access:
echo - Web interface: Click "Start Voice Call" at http://localhost:8080/
echo - Direct phone: Call %TWILIO_PHONE_NUMBER%
echo.

timeout /t 3 /nobreak >nul

echo Opening web interface in browser...
start http://localhost:8080/

echo.
echo ======================================
echo Full restart complete
echo.
echo Press Ctrl+C in each server window to stop the services.
echo ====================================== 