# Barbeque Nation Chatbot

A voice and text-enabled virtual assistant for Barbeque Nation restaurant, powered by Retell AI and Twilio. This chatbot helps customers get information about outlets, menu items, and make restaurant reservations.

Knowledge Base API Endpoints - https://dashboard.retellai.com/knowledgeBase?knowledge_base_id=knowledge_base_75f8f20bd2eb12a1
Post-Call Analysis Excel Sheet - https://docs.google.com/spreadsheets/d/1lbYDrqNNokr_FTEL5FfLXZHEIH-ZNKOp2LtI8LaARMY/edit?gid=0#gid=0
Chatbot Link - Due to Chatbot Retell Api being paid, the service currently was only able to run locally.
Agent Linked Phone Number - +1 (978) 718-5545

## Features

- **Text Chat Interface**: Web-based chat interface for customer queries
- **Voice Call Integration**: Voice calling functionality using Retell AI and Twilio
- **Direct Phone Number**: Dedicated Twilio phone line (+1 978-718-5545) for voice interactions
- **Enhanced Knowledge Base**: Comprehensive database with detailed menu items and outlet information
- **Structured Conversation Flow**: State-based flow for booking reservations
- **Fallback Mechanism**: Local knowledge base fallback when API is unavailable
- **Special Diet Support**: Information about Jain food, gluten-free, and low-calorie options
- **Outlet Details**: Comprehensive information about locations in Bangalore and Delhi

## Architecture

The application consists of two main components:

1. **Python Server** (port 8000):
   - Knowledge Base API
   - Webhook API for call logging

2. **Go Server** (port 8080):
   - Web UI (HTML, CSS, JavaScript)
   - API endpoints for chatbot functionality
   - Retell AI and Twilio integration

## Prerequisites

- Python 3.8+ with pip
- Go 1.16+
- Retell AI account and API key
- Agent ID from Retell AI dashboard
- Twilio phone number (provided: +1 978-718-5545)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/bbq-nation-chatbot.git
   cd bbq-nation-chatbot
   ```

2. Create a `.env` file in the root directory:
   ```
   RETELL_API_KEY=your_retell_api_key
   DEFAULT_AGENT_ID=your_agent_id
   KNOWLEDGE_BASE_ID=your_knowledge_base_id
   TWILIO_PHONE_NUMBER=+19787185545
   USE_TWILIO_DIRECT=false
   PORT=8000
   GO_PORT=8080
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install Go dependencies:
   ```
   go mod download
   ```

## Voice Calling Options

The chatbot supports two voice calling methods:

1. **Web-based calling**: Using Retell's web SDK for in-browser voice calls
2. **Direct phone calling**: Using the Twilio phone number (+1 978-718-5545)

You can configure the preferred calling method in the `.env` file:
- Set `USE_TWILIO_DIRECT=true` to always use direct phone calling
- Set `USE_TWILIO_DIRECT=false` to use web-based calling with phone as fallback

For more details on phone integration, see the [PHONE_GUIDE.md](PHONE_GUIDE.md) file.

## Knowledge Base Information

The chatbot provides detailed information about:

- **Restaurant Outlets**: 5 locations in Bangalore and 4 locations in Delhi with:
  - Addresses and contact numbers
  - Opening hours (lunch and dinner)
  - Facilities (bar, wheelchair access, etc.)
  - Parking information
  - Special features

- **Menu Items**:
  - Detailed vegetarian and non-vegetarian starters with descriptions
  - Main course options with ingredients
  - Dessert varieties including kulfi flavors
  - Beverages (mocktails, soft drinks, juices)
  - Special dietary options (Jain, gluten-free, low-calorie)

- **Offers and Combos**:
  - Weekday lunch specials
  - Birthday and anniversary offers
  - Corporate packages

## Configuration

Before running the application, check your setup using the provided configuration checker:

```
check_setup.bat
```

This will validate your environment, API keys, and dependencies.

## Running the Application

1. Using the convenience script (Windows):
   ```
   run.bat
   ```

2. Or start the servers manually:
   ```
   # Terminal 1 - Python server
   python server.py

   # Terminal 2 - Go server
   cd chatbot
   go run server.go
   ```

3. Access the web UI at http://localhost:8080/

## Troubleshooting

If you encounter any issues, try the following:

1. **API Connection Issues**:
   Run the API check utility:
   ```
   check_retell_api.bat
   ```

2. **Phone Integration Issues**:
   Verify phone configuration with:
   ```
   check_phone.bat
   ```

3. **Server Restart**:
   Restart both servers using:
   ```
   full_restart.bat
   ```

4. **Common Errors**:
   - "Cannot POST /v1/create-web-call": Check your Retell API key or try using the direct phone number
   - "Error: Could not start call": Use the provided phone number alternative
   - Connection errors: Check if both servers are running

## Directory Structure

```
bbq-nation-chatbot/
├── chatbot/               # Go server and API
│   ├── static/            # Web UI assets
│   │   ├── css/           # Stylesheets
│   │   ├── js/            # JavaScript files
│   │   └── img/           # Images
│   ├── server.go          # Go server entry point
│   └── api.go             # API implementation
├── knowledge_base/        # Knowledge base implementation
│   ├── api.py             # KB API endpoints
│   └── data.py            # Restaurant data
├── webhook/               # Webhook implementation
│   └── api.py             # Webhook endpoints
├── server.py              # Python server entry point
├── .env.example           # Example environment variables
├── requirements.txt       # Python dependencies
├── PHONE_GUIDE.md         # Twilio phone integration guide
├── run.bat                # Startup script (Windows)
├── run.sh                 # Startup script (Linux/macOS)
└── README.md              # This file
```

## Utility Scripts

- `check_retell_api.bat`: Tests Retell API connectivity
- `check_setup.bat`: Validates environment setup
- `check_phone.bat`: Validates phone number configuration
- `full_restart.bat`: Stops and restarts all servers
- `test_retell_api.py`: Python script to test API connectivity

## Conversation Flow

The chatbot implements a state-based conversation flow for restaurant bookings:

1. **Greeting**: Initial greeting and purpose identification
2. **City Selection**: Choose between Delhi and Bangalore
3. **Outlet Selection**: Select a specific restaurant location
4. **Reservation Details**: Date, time, and party size
5. **Contact Information**: Phone number for confirmation
6. **Confirmation**: Verify booking details
7. **End**: Provide booking reference

## License

[MIT License](LICENSE)

## Acknowledgements

- [Retell AI](https://retellai.com) for voice AI capabilities
- [Twilio](https://twilio.com) for telephony services
- [Gin Web Framework](https://github.com/gin-gonic/gin) for Go server
- [FastAPI](https://fastapi.tiangolo.com/) for Python API 
