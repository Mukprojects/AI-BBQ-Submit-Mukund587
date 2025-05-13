@echo off
echo ======================================
echo Barbeque Nation Chatbot - Phone Check
echo ======================================

REM Load the phone number from .env
for /f "tokens=*" %%a in ('type .env ^| findstr "TWILIO_PHONE_NUMBER"') do (
    set %%a
)

if "%TWILIO_PHONE_NUMBER%"=="" (
    echo ERROR: TWILIO_PHONE_NUMBER not found in .env file
    echo Please add the following line to your .env file:
    echo TWILIO_PHONE_NUMBER=+19787185545
    goto end
)

echo.
echo Twilio phone number is configured: %TWILIO_PHONE_NUMBER%
echo.
echo Testing phone number format...

REM Simple regex check for phone number format
echo %TWILIO_PHONE_NUMBER% | findstr /r "\+[0-9][0-9]*" >nul
if %errorlevel% neq 0 (
    echo ERROR: Phone number format is invalid. It should start with + followed by digits.
    goto end
)

echo Phone number format appears valid.
echo.
echo To manually test the phone number:
echo 1. Call %TWILIO_PHONE_NUMBER% directly from your phone
echo 2. Or click "Start Voice Call" in the web interface to get call options
echo.
echo Troubleshooting tips:
echo - If calling the number doesn't connect to the agent, check that Twilio and Retell are properly configured
echo - Ensure the DEFAULT_AGENT_ID is correctly set in your .env file
echo - Try toggling USE_TWILIO_DIRECT=true in your .env file for direct calling mode
echo.

:end
echo ======================================
pause 