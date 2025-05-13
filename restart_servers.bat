@echo off
echo ======================================
echo Barbeque Nation Chatbot - Restarting Servers
echo ======================================

echo Stopping any existing servers...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM go.exe >nul 2>&1

echo.
echo Copying .env file to chatbot directory...
copy /Y .env chatbot\.env >nul 2>&1

echo.
echo Starting Python server (port 8000)...
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
echo Press Ctrl+C in each server window to stop the services.
echo Opening web interface in browser...

timeout /t 3 /nobreak >nul
start http://localhost:8080/

echo ====================================== 