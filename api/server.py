"""
Main API Server

This module sets up the FastAPI server that includes all endpoints,
including the knowledge base API.
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the knowledge base API
from knowledge_base import kb_app

# Load environment variables
load_dotenv()
PORT = int(os.getenv("PORT", "8000"))

# Create main FastAPI app
app = FastAPI(
    title="Barbeque Nation Chatbot API",
    description="API for Barbeque Nation chatbot and voice agent",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, for development only
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount the knowledge base API
app.mount("/kb", kb_app)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Barbeque Nation Chatbot API",
        "endpoints": [
            "/kb - Knowledge Base API",
            "/webhook - Webhook API (coming soon)",
            "/chatbot - Chatbot API (coming soon)"
        ]
    }

# Version endpoint
@app.get("/version")
async def version():
    return {"version": "1.0.0"}

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, reload=True) 