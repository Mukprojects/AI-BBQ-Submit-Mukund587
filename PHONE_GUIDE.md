# Twilio Phone Integration Guide

This guide explains how to use the Twilio phone integration with the BBQ Nation Chatbot.

## Phone Number

The chatbot is accessible through the following phone number:
**+1 (978) 718-5545**

## Configuration Options

The chatbot supports two modes for voice interaction:

### 1. Web-to-Phone Integration (Default)

In this mode, the web interface attempts to establish a call using the Retell Web SDK first, but provides the phone number as a fallback option.

**Configuration:**
```
USE_TWILIO_DIRECT=false
TWILIO_PHONE_NUMBER=+19787185545
```

### 2. Direct Phone-Only Mode

In this mode, the web interface will always display the phone number to call directly, bypassing the Retell Web SDK.

**Configuration:**
```
USE_TWILIO_DIRECT=true
TWILIO_PHONE_NUMBER=+19787185545
```

## How to Use the Phone Integration

### From the Web Interface

1. Navigate to the chatbot web interface at http://localhost:8080/
2. Click the "Start Voice Call" button
3. Depending on your configuration:
   - In Web-to-Phone mode: The interface will try to establish a web call first, with the phone number as a fallback
   - In Direct Phone mode: The interface will display the phone number to call

### Direct Calling

You can call the phone number directly from any phone:

1. Dial +1 (978) 718-5545 from your phone
2. The BBQ Nation agent will answer and assist you with your query

## Troubleshooting

If you encounter issues with the phone integration:

1. **Check your configuration**: Verify that the `TWILIO_PHONE_NUMBER` is correctly set in your `.env` file
2. **Test the phone connectivity**: Run `check_phone.bat` to verify the phone number configuration
3. **Try direct mode**: Set `USE_TWILIO_DIRECT=true` in your `.env` file to bypass the web SDK
4. **Restart the servers**: Run `full_restart.bat` to restart all services
5. **Check logs**: Look for any error messages in the server logs that might indicate connection issues

## Implementation Details

The Twilio phone integration works through:

1. The Retell API with agent ID configuration (for web-to-phone calls)
2. Direct Twilio number (for phone-only mode)

When using the web interface, the system will always provide the phone number as an alternative option if web calling fails for any reason. 