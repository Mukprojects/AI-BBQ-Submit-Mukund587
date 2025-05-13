"""
Test Retell API Connectivity

This script tests the connection to the Retell API and verifies if the API key is valid.
"""

import os
import requests
import json
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Get Retell API key from environment
retell_api_key = os.getenv("RETELL_API_KEY")
if not retell_api_key:
    print("Error: RETELL_API_KEY is not set in environment")
    sys.exit(1)

# Get agent ID from environment
agent_id = os.getenv("DEFAULT_AGENT_ID")
if not agent_id:
    print("Warning: DEFAULT_AGENT_ID is not set in environment")
    # Not exiting as we can still test the API key validity

# Define Retell API URL
retell_base_url = "https://api.retellai.com/v1"

def test_api_key():
    """Test if the API key is valid by making a simple request"""
    
    print(f"Testing API key: {retell_api_key[:4]}...{retell_api_key[-4:] if len(retell_api_key) > 8 else '****'}")
    
    try:
        # Try to get agents list as a simple API test
        headers = {
            "Authorization": f"Bearer {retell_api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(f"{retell_base_url}/agents", headers=headers)
        
        if response.status_code == 200:
            print("✅ API key is valid")
            print(f"Response: {response.status_code} {response.reason}")
            return True
        else:
            print(f"❌ API key validation failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return False

def test_agent_id():
    """Test if the agent ID is valid"""
    
    if not agent_id:
        print("Skipping agent ID test as DEFAULT_AGENT_ID is not set")
        return False
        
    print(f"Testing agent ID: {agent_id}")
    
    try:
        # Try to get agent details
        headers = {
            "Authorization": f"Bearer {retell_api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(f"{retell_base_url}/agents/{agent_id}", headers=headers)
        
        if response.status_code == 200:
            agent_data = response.json()
            print(f"✅ Agent ID is valid: {agent_data.get('name', 'Unknown agent name')}")
            return True
        else:
            print(f"❌ Agent ID validation failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing agent ID: {e}")
        return False

def test_simple_conversation():
    """Test a simple text conversation with the agent"""
    
    if not agent_id:
        print("Skipping conversation test as DEFAULT_AGENT_ID is not set")
        return False
        
    print(f"Testing simple conversation with agent ID: {agent_id}")
    
    try:
        # Create a simple conversation request
        headers = {
            "Authorization": f"Bearer {retell_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "agent_id": agent_id,
            "user_id": "test_user_1",
            "message": "Hello, I'd like to book a table at BBQ Nation",
            "mode": "text",
            "streaming": False
        }
        
        response = requests.post(f"{retell_base_url}/conversations", headers=headers, json=data)
        
        if response.status_code == 200:
            resp_data = response.json()
            print(f"✅ Conversation test successful")
            print(f"Agent response: {resp_data.get('response', 'No response')}")
            return True
        else:
            print(f"❌ Conversation test failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing conversation: {e}")
        return False

if __name__ == "__main__":
    print("Retell API Connection Test")
    print("==========================")
    print(f"Using API URL: {retell_base_url}")
    
    # Test API key
    api_key_valid = test_api_key()
    
    if api_key_valid:
        print("\nAPI key is valid, testing agent ID...")
        agent_id_valid = test_agent_id()
        
        if agent_id_valid:
            print("\nTesting simple conversation...")
            test_simple_conversation()
    
    print("\nTest completed") 