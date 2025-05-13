"""
Webhook API

This module implements the FastAPI endpoints for Retell webhooks.
"""

from fastapi import FastAPI, Request, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import json
import os
from dotenv import load_dotenv

# Import local modules
from .google_sheets import log_call_to_sheets

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Barbeque Nation Webhook API",
    description="API for handling Retell webhooks and post-call logging",
    version="1.0.0"
)

# Define webhook event types
class WebhookEvent(BaseModel):
    event_type: str
    payload: Dict[str, Any]

@app.get("/")
async def root():
    return {"message": "Barbeque Nation Webhook API"}

@app.post("/webhook")
async def handle_webhook(event: WebhookEvent):
    """Handle incoming webhook events from Retell."""
    
    event_type = event.event_type
    payload = event.payload
    
    if event_type == "call_started":
        # Just log call started event
        print(f"Call started: {payload}")
        return {"status": "success", "message": "Call started event received"}
    
    elif event_type == "call_ended":
        # Process and log call data
        try:
            # Extract call information
            call_data = {
                "modality": "Call",
                "phone_number": payload.get("phone_number", "NA"),
                "transcript": " ".join([turn.get("transcript", "") for turn in payload.get("turns", [])]),
            }
            
            # Log call to Google Sheets
            result = log_call_to_sheets(call_data)
            
            return result
        
        except Exception as e:
            print(f"Error processing call_ended event: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    elif event_type == "call_analyzed":
        # Process and log call analysis
        try:
            # Extract call information
            call_data = {
                "modality": "Call",
                "phone_number": payload.get("phone_number", "NA"),
                "transcript": payload.get("transcript", ""),
                "analysis": payload.get("analysis", {})
            }
            
            # Log call to Google Sheets
            result = log_call_to_sheets(call_data)
            
            return result
        
        except Exception as e:
            print(f"Error processing call_analyzed event: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    else:
        # Handle unknown event type
        return {"status": "warning", "message": f"Unknown event type: {event_type}"}

@app.post("/chatbot-log")
async def log_chatbot_conversation(
    data: Dict[str, Any] = Body(...)
):
    """
    Log chatbot conversation to Google Sheets.
    This endpoint is called when a chatbot conversation ends.
    """
    try:
        # Extract chatbot conversation information
        call_data = {
            "modality": "Chatbot",
            "phone_number": data.get("phone_number", "NA"),
            "transcript": data.get("transcript", "")
        }
        
        # Log chatbot conversation to Google Sheets
        result = log_call_to_sheets(call_data)
        
        return result
    
    except Exception as e:
        print(f"Error logging chatbot conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 