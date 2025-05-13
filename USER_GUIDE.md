# Barbeque Nation Chatbot User Guide

This guide will help you set up, run, and use the Barbeque Nation chatbot and voice assistant system.

## Prerequisites

- Python 3.8+ with pip
- Go 1.16+
- Retell.ai account with API key
- Google Cloud account for Sheets API (for call logging)
- Twilio account (for phone integration)

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file in the project root with the following variables:

```
# API Keys
RETELL_API_KEY=your_retell_api_key
DEFAULT_AGENT_ID=your_agent_id

# Twilio Configuration
TWILIO_PHONE_NUMBER=+19787185545
USE_TWILIO_DIRECT=false

# Configuration
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
PORT=8000
GO_PORT=8080
BOT_NAME=BBQ Nation Assistant
MAX_TOKENS=800

# Google Sheets
GOOGLE_SHEET_ID=your_google_sheet_id
```

### 2. Google Sheets Setup

1. Create a Google Cloud project
2. Enable the Google Sheets API
3. Create service account credentials
4. Download the JSON key file and place it in the project
5. Share your Google Sheet with the service account email
6. Add the following headers to the first row of your Google Sheet:
   - Call ID
   - Customer Phone
   - Date & Time
   - Duration
   - City
   - Outlet
   - Reservation Date
   - Reservation Time
   - Party Size
   - Status
   - Notes

### 3. Installation

#### Windows:
Run the `setup.bat` script to install all dependencies.

#### Linux/Mac:
Make the setup script executable:
```
chmod +x run.sh
```

Then install dependencies:
```
pip install -r requirements.txt
go mod download
```

## Running the System

### Windows:
Run the `run.bat` script to start both servers.

### Linux/Mac:
Run the shell script:
```
./run.sh
```

## Using the Chatbot

1. Open your web browser and navigate to `http://localhost:8080`
2. The chatbot interface will appear with a welcome message
3. You can type questions about:
   - Restaurant outlets in Delhi and Bangalore (5 in Bangalore, 4 in Delhi)
   - Menu items including vegetarian and non-vegetarian options
   - Special dietary needs (Jain, gluten-free, low-calorie options)
   - Desserts including 9 varieties of kulfi
   - Opening hours, facilities, and special offers
   - Make reservations

### Enhanced Knowledge Base

The chatbot has detailed knowledge about:

1. **Restaurant Outlets**:
   - Addresses and direct contact numbers for each location
   - Opening hours for lunch and dinner
   - Available facilities (wheelchair access, baby chairs, etc.)
   - Parking information
   - Special features unique to each outlet

2. **Menu Items**:
   - Detailed descriptions of starters with ingredients
   - Main course options for both vegetarians and non-vegetarians
   - Complete dessert menu including kulfi varieties
   - Beverage options (mocktails, soft drinks, juices)
   - Seasonal and special items

3. **Special Dietary Information**:
   - Jain food options (no root vegetables, no onion, no garlic)
   - Gluten-free alternatives
   - Low-calorie options for health-conscious customers
   - Seafood availability

4. **Offers and Promotions**:
   - Weekday lunch special discounts
   - Birthday and anniversary celebrations
   - Corporate packages for large groups

### Voice Call Features

#### Web-Based Voice Call:
1. Click the "Start Voice Call" button in the chatbot interface
2. The system will connect to the Retell AI service
3. Speak naturally to the voice assistant
4. The assistant will guide you through the same capabilities as the text interface

#### Direct Phone Call:
1. Dial the dedicated phone number: **+1 (978) 718-5545**
2. Speak directly with the BBQ Nation voice assistant
3. Access all the same information and services as the web interface

You can also find detailed phone integration instructions in the PHONE_GUIDE.md file.

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify your API keys are correct in the `.env` file
   - Check internet connection
   - Run `check_retell_api.bat` to test API connectivity

2. **Google Sheets Integration**
   - Ensure the service account has editing permissions to the Google Sheet
   - Verify the GOOGLE_SHEET_ID is correct

3. **Server Startup Issues**
   - Check port conflicts (default ports are 8000 and 8080)
   - Verify all dependencies are installed
   - Run `check_servers.bat` to verify services are running

4. **Voice Call Not Working**
   - Check browser compatibility (Chrome recommended)
   - Ensure microphone permissions are granted
   - Try the direct phone number as an alternative
   - Run `check_phone.bat` to verify phone configuration

## API Documentation

Visit `http://localhost:8000/kb/docs` for the full Knowledge Base API documentation. 