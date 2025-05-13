"""
Barbeque Nation Chatbot Main Server

This script runs the combined FastAPI server that includes:
- Knowledge Base API
- Webhook API for post-call logging
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import APIs
from knowledge_base import kb_app
from webhook.api import app as webhook_app

# Load environment variables
load_dotenv()
PORT = int(os.getenv("PORT", "8000"))

# Create FastAPI app
app = FastAPI(
    title="Barbeque Nation Chatbot API",
    description="API for Barbeque Nation chatbot and voice agent",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount sub-applications
app.mount("/kb", kb_app)
app.mount("/webhook", webhook_app)

@app.get("/")
async def root():
    return {
        "message": "Barbeque Nation Chatbot API",
        "endpoints": [
            "/kb - Knowledge Base API",
            "/webhook - Webhook API",
            "/docs - API Documentation"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print(f"Starting server on port {PORT}")
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, reload=True) 