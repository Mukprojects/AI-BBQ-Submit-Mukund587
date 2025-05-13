@echo off
echo ======================================
echo Barbeque Nation Chatbot - API Key Validation
echo ======================================

echo Checking Retell API key...
echo.

REM Check if PowerShell is available
where powershell >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PowerShell is not available. This script requires PowerShell.
    exit /b 1
)

REM Read API key from .env file and check its validity
powershell -Command "if (Test-Path .env) { $env = Get-Content .env | Where-Object { $_ -match '^[^#]' }; $retellApiKey = ($env | Where-Object { $_ -match 'RETELL_API_KEY' } | ForEach-Object { $_.Split('=')[1] }); echo \"Found API Key: $retellApiKey\"; echo \"API Key length: $($retellApiKey.Length) characters\"; if ($retellApiKey.Length -lt 20) { echo \"\nWARNING: The API key appears to be too short. Full Retell API keys are usually longer than 20 characters.\" }; $headers = @{Authorization = \"Bearer $retellApiKey\"}; try { $response = Invoke-WebRequest -Uri \"https://api.retellai.com/v1/agents\" -Headers $headers -Method GET -UseBasicParsing; echo \"\nAPI Key valid! Response:\"; $response.Content } catch { echo \"\nAPI Key check failed: $_\"; if ($_.Exception.Response.StatusCode.value__ -eq 401) { echo \"\nERROR: The API key is not valid. Please check that you have the complete API key.\" } } } else { echo \"ERROR: .env file not found!\" }"

echo.
echo ======================================
echo API Key check complete
echo ======================================
echo.
echo If the test failed with a 401 Unauthorized error, your API key is likely invalid.
echo.
echo To fix this:
echo 1. Go to the Retell Dashboard at https://dashboard.retellai.com/apiKey
echo 2. Create a new API key or copy your existing complete key
echo 3. Update the RETELL_API_KEY value in your .env file
echo 4. Run the restart_servers.bat script to apply changes
echo. 