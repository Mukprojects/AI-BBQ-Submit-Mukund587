# Barbeque Nation Chatbot Troubleshooting

## API Connection Issues

If you see these errors in your chatbot:
- `Cannot POST /v1/conversations`
- `Retell API error`

This is likely due to issues with the Retell API connection. Here's how to fix them:

### 1. Check your API key

Your Retell API key appears to be incomplete. Complete Retell API keys are usually longer than 20 characters.

To get a valid API key:
1. Go to the Retell Dashboard at https://dashboard.retellai.com/apiKey
2. Create a new API key or copy your existing complete key
3. Update the `RETELL_API_KEY` value in your `.env` file

Example of a properly formatted API key:
```
RETELL_API_KEY=key_9ac7e63347dbab6b9fc2eae04de12345678901234567890
```

### 2. Check your Agent ID

Make sure your agent ID is in the correct format. It should start with `ag_` (which we've already fixed in your config).

### 3. Testing your API connection

Use these utility scripts to check your connection:

- `check_api_key.bat` - Tests if your API key is valid
- `check_retell_api.bat` - Tests if your agent ID is valid
- `check_servers.bat` - Checks if your servers are running properly

### 4. Restarting servers

After making changes to your `.env` file, run:
```
restart_servers.bat
```

This will stop any running servers and restart them with the new configuration.

## Knowledge Base Integration

The knowledge base is not directly related to the API connection issues but provides content for your chatbot.

To use the knowledge base:
1. Make sure the Python server is running on port 8000
2. This server exposes the knowledge base API at http://localhost:8000/kb
3. The Python server also hosts the webhook API at http://localhost:8000/webhook

## Additional Help

If you still encounter issues:
1. Check the terminal output for error messages
2. Visit http://localhost:8080/api/debug to see the API configuration
3. Make sure both servers are running (Python on port 8000, Go on port 8080) 