@echo off
echo ======================================
echo Barbeque Nation Chatbot Server Check
echo ======================================

echo Checking Python server (port 8000)...
powershell -Command "try { $response = Invoke-WebRequest -Uri http://localhost:8000 -UseBasicParsing -TimeoutSec 5; echo 'Python server is running! Status code:' $response.StatusCode } catch { echo 'Python server is NOT running or not accessible!' }"

echo.
echo Checking Go server (port 8080)...
powershell -Command "try { $response = Invoke-WebRequest -Uri http://localhost:8080 -UseBasicParsing -TimeoutSec 5; echo 'Go server is running! Status code:' $response.StatusCode } catch { echo 'Go server is NOT running or not accessible!' }"

echo.
echo Checking API endpoints...
echo.

echo Checking Chatbot API (start endpoint)...
powershell -Command "try { $response = Invoke-WebRequest -Uri http://localhost:8080/api/chatbot/start -Method POST -Body '{\"user_id\":\"test_user\"}' -ContentType 'application/json' -UseBasicParsing -TimeoutSec 5; echo 'API endpoint is accessible! Response:'; $response.Content } catch { echo 'API endpoint error:' $_.Exception.Message }"

echo.
echo Checking environment variables...
echo.

powershell -Command "if (Test-Path .env) { echo '.env file exists and contains:'; Get-Content .env | ForEach-Object { if ($_ -match '^[^#]') { echo $_ } } } else { echo '.env file does not exist!' }"

echo.
echo ======================================
echo Server check complete
echo ====================================== 