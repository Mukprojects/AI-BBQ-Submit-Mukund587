"""
Google Sheets Integration

This module handles the integration with Google Sheets API for post-call logging.
"""

import os
import json
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import gspread
from datetime import datetime
import re

# Load environment variables
load_dotenv()
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_SERVICE_ACCOUNT_EMAIL = os.getenv("GOOGLE_SERVICE_ACCOUNT_EMAIL")
GOOGLE_PRIVATE_KEY = os.getenv("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n")

# Define spreadsheet columns
COLUMNS = [
    "Modality",
    "Call Time",
    "Phone Number",
    "Call Outcome",
    "Booking Date",
    "Booking Time",
    "Customer Name",
    "Number of Guests",
    "Call Summary"
]

def init_google_sheets_client():
    """Initialize the Google Sheets client."""
    try:
        # Create credentials
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = {
            "type": "service_account",
            "project_id": "bbq-nation-chatbot",
            "private_key_id": "private_key_id",
            "private_key": GOOGLE_PRIVATE_KEY,
            "client_email": GOOGLE_SERVICE_ACCOUNT_EMAIL,
            "client_id": "client_id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{GOOGLE_SERVICE_ACCOUNT_EMAIL}"
        }
        
        # Create a Credentials object
        creds = Credentials.from_service_account_info(credentials, scopes=scopes)
        
        # Create gspread client
        client = gspread.authorize(creds)
        
        return client
    except Exception as e:
        print(f"Error initializing Google Sheets client: {e}")
        return None

def get_call_outcome(transcript):
    """
    Determine the call outcome based on the transcript.
    
    Returns one of:
    - Enquiry: Customer asking a general question
    - Availability: Customer looking to book
    - Post-Booking: Customer calling about existing reservation
    - Misc: Any other reason
    """
    transcript_lower = transcript.lower()
    
    # Check for booking-related keywords
    if any(word in transcript_lower for word in ["book", "reservation", "table", "available"]):
        return "Availability"
    
    # Check for post-booking keywords
    elif any(word in transcript_lower for word in ["change", "modify", "cancel", "update", "existing"]):
        return "Post-Booking"
    
    # Check for enquiry keywords
    elif any(word in transcript_lower for word in ["menu", "hour", "time", "open", "address", "location", "parking"]):
        return "Enquiry"
    
    # Default to Misc
    else:
        return "Misc."

def extract_booking_date(transcript):
    """Extract booking date from transcript."""
    # Try to find dates in format YYYY-MM-DD
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    dates = re.findall(date_pattern, transcript)
    
    if dates:
        return dates[0]
    
    # Try to find dates in format DD/MM/YYYY or MM/DD/YYYY
    date_pattern = r'\d{1,2}/\d{1,2}/\d{4}'
    dates = re.findall(date_pattern, transcript)
    
    if dates:
        # Convert to YYYY-MM-DD format
        date_parts = dates[0].split('/')
        if len(date_parts) == 3:
            return f"{date_parts[2]}-{date_parts[1].zfill(2)}-{date_parts[0].zfill(2)}"
    
    # Try to find common date phrases
    if "today" in transcript.lower():
        return datetime.now().strftime("%Y-%m-%d")
    elif "tomorrow" in transcript.lower():
        tomorrow = datetime.now() + datetime.timedelta(days=1)
        return tomorrow.strftime("%Y-%m-%d")
    
    return "NA"

def extract_booking_time(transcript):
    """Extract booking time from transcript."""
    # Try to find times in format HH:MM
    time_pattern = r'\d{1,2}:\d{2}'
    times = re.findall(time_pattern, transcript)
    
    if times:
        return times[0]
    
    # Try to find times with AM/PM
    time_pattern = r'\d{1,2}(?::\d{2})?\s*(?:am|pm)'
    times = re.findall(time_pattern, transcript.lower())
    
    if times:
        time = times[0]
        # Convert to HH:MM format
        if ":" not in time:
            hour = int(re.findall(r'\d+', time)[0])
            if "pm" in time and hour < 12:
                hour += 12
            elif "am" in time and hour == 12:
                hour = 0
            return f"{hour:02d}:00"
        else:
            hour, minute = map(int, re.findall(r'\d+', time)[:2])
            if "pm" in time and hour < 12:
                hour += 12
            elif "am" in time and hour == 12:
                hour = 0
            return f"{hour:02d}:{minute:02d}"
    
    return "NA"

def extract_party_size(transcript):
    """Extract party size from transcript."""
    # Look for phrases like "for 4 people" or "party of 6"
    size_patterns = [
        r'for\s+(\d+)\s+people',
        r'for\s+(\d+)\s+person',
        r'party\s+of\s+(\d+)',
        r'(\d+)\s+guests',
        r'(\d+)\s+people',
        r'(\d+)\s+person',
        r'table\s+for\s+(\d+)',
        r'booking\s+for\s+(\d+)'
    ]
    
    for pattern in size_patterns:
        matches = re.findall(pattern, transcript.lower())
        if matches:
            return matches[0]
    
    return "NA"

def extract_customer_name(transcript):
    """
    Extract customer name from transcript.
    This is a simplified approach - in real-world scenarios,
    you would use NER (Named Entity Recognition) for better accuracy.
    """
    # Look for phrases like "my name is John" or "name's John"
    name_patterns = [
        r'my name is (\w+)',
        r"name's (\w+)",
        r'name is (\w+)',
        r'I am (\w+)',
        r"I'm (\w+)",
    ]
    
    for pattern in name_patterns:
        matches = re.findall(pattern, transcript.lower())
        if matches:
            return matches[0].capitalize()
    
    return "NA"

def generate_call_summary(transcript, outcome, date, time, party_size):
    """Generate a summary of the call for logging."""
    summary = f"Customer called about "
    
    if outcome == "Enquiry":
        # Extract what they were inquiring about
        if "menu" in transcript.lower():
            summary += "the menu."
        elif "hour" in transcript.lower() or "time" in transcript.lower() or "open" in transcript.lower():
            summary += "opening hours."
        elif "address" in transcript.lower() or "location" in transcript.lower():
            summary += "restaurant location."
        elif "parking" in transcript.lower():
            summary += "parking facilities."
        else:
            summary += "general information."
    
    elif outcome == "Availability":
        if date != "NA" and time != "NA":
            summary += f"making a reservation for {date} at {time}"
            if party_size != "NA":
                summary += f" for {party_size} guests."
            else:
                summary += "."
        else:
            summary += "checking availability."
    
    elif outcome == "Post-Booking":
        if "cancel" in transcript.lower():
            summary += "cancelling a reservation."
        elif "change" in transcript.lower() or "modify" in transcript.lower() or "update" in transcript.lower():
            summary += "modifying an existing reservation."
        else:
            summary += "an existing reservation."
    
    else:  # Misc
        summary += "a miscellaneous matter."
    
    return summary

def log_call_to_sheets(call_data):
    """
    Log call data to Google Sheets.
    
    call_data should be a dictionary with:
    - modality: "Call" or "Chatbot"
    - phone_number: Customer's phone number
    - transcript: Full call transcript
    """
    try:
        # Initialize Google Sheets client
        client = init_google_sheets_client()
        if not client:
            return {"error": "Failed to initialize Google Sheets client"}
        
        # Open the spreadsheet
        sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1
        
        # Process the call data
        modality = call_data.get("modality", "Call")
        phone_number = call_data.get("phone_number", "NA")
        transcript = call_data.get("transcript", "")
        call_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Determine call outcome
        outcome = get_call_outcome(transcript)
        
        # Extract booking details
        booking_date = extract_booking_date(transcript)
        booking_time = extract_booking_time(transcript)
        party_size = extract_party_size(transcript)
        customer_name = extract_customer_name(transcript)
        
        # Generate call summary
        call_summary = generate_call_summary(transcript, outcome, booking_date, booking_time, party_size)
        
        # Prepare row data
        row_data = [
            modality,
            call_time,
            phone_number,
            outcome,
            booking_date,
            booking_time,
            customer_name,
            party_size,
            call_summary
        ]
        
        # Append row to spreadsheet
        sheet.append_row(row_data)
        
        return {"status": "success", "message": "Call logged successfully"}
    
    except Exception as e:
        print(f"Error logging call to Google Sheets: {e}")
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Test with a sample call
    sample_call = {
        "modality": "Call",
        "phone_number": "9876543210",
        "transcript": "Hello, I would like to make a reservation for 4 people on 2023-05-15 at 7:30 PM. My name is John."
    }
    result = log_call_to_sheets(sample_call)
    print(result) 