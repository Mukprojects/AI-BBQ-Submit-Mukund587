"""
Retell Integration

This module handles the integration with Retell API for the conversation flow.
It defines the functions to create and manage Retell conversation flows.
"""

import os
import requests
import json
from dotenv import load_dotenv
from jinja2 import Template
from .templates import TEMPLATES

# Load environment variables
load_dotenv()
RETELL_API_KEY = os.getenv("RETELL_API_KEY")

# Retell API endpoints
RETELL_BASE_URL = "https://api.retellai.com/v1"
RETELL_AGENTS_URL = f"{RETELL_BASE_URL}/agents"
RETELL_FLOWS_URL = f"{RETELL_BASE_URL}/flows"
RETELL_NODES_URL = f"{RETELL_BASE_URL}/nodes"
RETELL_EDGES_URL = f"{RETELL_BASE_URL}/edges"

# Headers for Retell API requests
HEADERS = {
    "Authorization": f"Bearer {RETELL_API_KEY}",
    "Content-Type": "application/json"
}

def create_agent(name, description, voice_id="matthew"):
    """Create a new Retell agent."""
    payload = {
        "name": name,
        "description": description,
        "voice_id": voice_id,
        "llm": "gpt-4"
    }
    
    response = requests.post(RETELL_AGENTS_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error creating agent: {response.text}")
        return None

def create_flow(agent_id, name, description):
    """Create a new conversation flow for an agent."""
    payload = {
        "agent_id": agent_id,
        "name": name,
        "description": description
    }
    
    response = requests.post(RETELL_FLOWS_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error creating flow: {response.text}")
        return None

def create_node(flow_id, name, state_name, template_variables=None):
    """Create a new node in a conversation flow."""
    # Get the template for this state
    template_str = TEMPLATES.get(state_name, "")
    
    # Render the template with variables (if provided)
    if template_variables:
        template = Template(template_str)
        prompt = template.render(**template_variables)
    else:
        prompt = template_str
    
    payload = {
        "flow_id": flow_id,
        "name": name,
        "prompt": prompt
    }
    
    response = requests.post(RETELL_NODES_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error creating node: {response.text}")
        return None

def create_edge(flow_id, from_node_id, to_node_id, condition):
    """Create an edge between two nodes in a conversation flow."""
    payload = {
        "flow_id": flow_id,
        "from_node_id": from_node_id,
        "to_node_id": to_node_id,
        "condition": condition
    }
    
    response = requests.post(RETELL_EDGES_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error creating edge: {response.text}")
        return None

def create_bbq_nation_flow():
    """Create the complete Barbeque Nation conversation flow."""
    # Create an agent
    agent = create_agent(
        name="BBQ Nation Assistant",
        description="Voice assistant for Barbeque Nation restaurants in Delhi and Bangalore",
        voice_id="matthew"  # Use a male voice
    )
    
    if not agent:
        return None
    
    agent_id = agent["id"]
    
    # Create a flow
    flow = create_flow(
        agent_id=agent_id,
        name="BBQ Nation Booking Flow",
        description="Flow for handling restaurant inquiries and reservations for Barbeque Nation"
    )
    
    if not flow:
        return None
    
    flow_id = flow["id"]
    
    # Create nodes for each state
    nodes = {}
    
    # Create greeting node
    nodes["greeting"] = create_node(
        flow_id=flow_id,
        name="Greeting",
        state_name="greeting"
    )
    
    # Create city collection node
    nodes["city_collection"] = create_node(
        flow_id=flow_id,
        name="City Collection",
        state_name="city_collection"
    )
    
    # Create outlet collection node
    nodes["outlet_collection"] = create_node(
        flow_id=flow_id,
        name="Outlet Collection",
        state_name="outlet_collection",
        template_variables={"city": "{{city}}"}
    )
    
    # Create intent identification node
    nodes["intent_identification"] = create_node(
        flow_id=flow_id,
        name="Intent Identification",
        state_name="intent_identification",
        template_variables={"city": "{{city}}", "outlet": "{{outlet}}"}
    )
    
    # Create information inquiry node
    nodes["information_inquiry"] = create_node(
        flow_id=flow_id,
        name="Information Inquiry",
        state_name="information_inquiry",
        template_variables={"city": "{{city}}", "outlet": "{{outlet}}"}
    )
    
    # Create new reservation node
    nodes["new_reservation"] = create_node(
        flow_id=flow_id,
        name="New Reservation",
        state_name="new_reservation",
        template_variables={
            "city": "{{city}}",
            "outlet": "{{outlet}}",
            "date": "{{date}}",
            "time": "{{time}}",
            "party_size": "{{party_size}}",
            "customer_name": "{{customer_name}}",
            "phone_number": "{{phone_number}}"
        }
    )
    
    # Create reservation confirmation node
    nodes["reservation_confirmation"] = create_node(
        flow_id=flow_id,
        name="Reservation Confirmation",
        state_name="reservation_confirmation",
        template_variables={
            "city": "{{city}}",
            "outlet": "{{outlet}}",
            "date": "{{date}}",
            "time": "{{time}}",
            "party_size": "{{party_size}}",
            "customer_name": "{{customer_name}}",
            "phone_number": "{{phone_number}}"
        }
    )
    
    # Create modify reservation node
    nodes["modify_reservation"] = create_node(
        flow_id=flow_id,
        name="Modify Reservation",
        state_name="modify_reservation",
        template_variables={
            "city": "{{city}}",
            "outlet": "{{outlet}}",
            "customer_name": "{{customer_name}}",
            "reservation_date": "{{reservation_date}}",
            "modification_type": "{{modification_type}}",
            "new_date": "{{new_date}}",
            "new_time": "{{new_time}}",
            "new_party_size": "{{new_party_size}}"
        }
    )
    
    # Create cancel reservation node
    nodes["cancel_reservation"] = create_node(
        flow_id=flow_id,
        name="Cancel Reservation",
        state_name="cancel_reservation",
        template_variables={
            "city": "{{city}}",
            "outlet": "{{outlet}}",
            "customer_name": "{{customer_name}}",
            "reservation_date": "{{reservation_date}}",
            "confirmation": "{{confirmation}}"
        }
    )
    
    # Create fallback node
    nodes["fallback"] = create_node(
        flow_id=flow_id,
        name="Fallback",
        state_name="fallback"
    )
    
    # Create farewell node
    nodes["farewell"] = create_node(
        flow_id=flow_id,
        name="Farewell",
        state_name="farewell",
        template_variables={
            "city": "{{city}}",
            "outlet": "{{outlet}}",
            "date": "{{date}}",
            "time": "{{time}}"
        }
    )
    
    # Create edges between nodes
    
    # Greeting to City Collection
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["greeting"]["id"],
        to_node_id=nodes["city_collection"]["id"],
        condition="true"  # Always transition after greeting
    )
    
    # City Collection to Outlet Collection
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["city_collection"]["id"],
        to_node_id=nodes["outlet_collection"]["id"],
        condition="city != null && (transcript.toLowerCase().includes('delhi') || transcript.toLowerCase().includes('bangalore'))"
    )
    
    # Outlet Collection to Intent Identification
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["outlet_collection"]["id"],
        to_node_id=nodes["intent_identification"]["id"],
        condition="outlet != null"
    )
    
    # Intent Identification to Information Inquiry
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["intent_identification"]["id"],
        to_node_id=nodes["information_inquiry"]["id"],
        condition="transcript.toLowerCase().includes('information') || transcript.toLowerCase().includes('menu') || transcript.toLowerCase().includes('hour') || transcript.toLowerCase().includes('facilities') || transcript.toLowerCase().includes('parking')"
    )
    
    # Intent Identification to New Reservation
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["intent_identification"]["id"],
        to_node_id=nodes["new_reservation"]["id"],
        condition="transcript.toLowerCase().includes('reservation') || transcript.toLowerCase().includes('book') || transcript.toLowerCase().includes('table')"
    )
    
    # Intent Identification to Modify Reservation
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["intent_identification"]["id"],
        to_node_id=nodes["modify_reservation"]["id"],
        condition="transcript.toLowerCase().includes('modify') || transcript.toLowerCase().includes('change') || transcript.toLowerCase().includes('update')"
    )
    
    # Intent Identification to Cancel Reservation
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["intent_identification"]["id"],
        to_node_id=nodes["cancel_reservation"]["id"],
        condition="transcript.toLowerCase().includes('cancel')"
    )
    
    # Information Inquiry to Farewell
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["information_inquiry"]["id"],
        to_node_id=nodes["farewell"]["id"],
        condition="transcript.toLowerCase().includes('thank you') || transcript.toLowerCase().includes('thanks') || transcript.toLowerCase().includes('goodbye')"
    )
    
    # New Reservation to Reservation Confirmation
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["new_reservation"]["id"],
        to_node_id=nodes["reservation_confirmation"]["id"],
        condition="date != null && time != null && party_size != null && customer_name != null && phone_number != null"
    )
    
    # Reservation Confirmation to Farewell
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["reservation_confirmation"]["id"],
        to_node_id=nodes["farewell"]["id"],
        condition="true"  # Always transition after confirmation
    )
    
    # Modify Reservation to Farewell
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["modify_reservation"]["id"],
        to_node_id=nodes["farewell"]["id"],
        condition="transcript.toLowerCase().includes('thank you') || transcript.toLowerCase().includes('thanks') || transcript.toLowerCase().includes('goodbye')"
    )
    
    # Cancel Reservation to Farewell
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["cancel_reservation"]["id"],
        to_node_id=nodes["farewell"]["id"],
        condition="confirmation == 'yes'"
    )
    
    # Fallback to City Collection
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["fallback"]["id"],
        to_node_id=nodes["city_collection"]["id"],
        condition="transcript.toLowerCase().includes('start over') || transcript.toLowerCase().includes('restart')"
    )
    
    # Fallback to Farewell
    create_edge(
        flow_id=flow_id,
        from_node_id=nodes["fallback"]["id"],
        to_node_id=nodes["farewell"]["id"],
        condition="transcript.toLowerCase().includes('goodbye') || transcript.toLowerCase().includes('bye')"
    )
    
    return {
        "agent": agent,
        "flow": flow,
        "nodes": nodes
    }

def get_flow_details(flow_id):
    """Get details for a conversation flow."""
    response = requests.get(f"{RETELL_FLOWS_URL}/{flow_id}", headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting flow details: {response.text}")
        return None

def purchase_phone_number(agent_id):
    """Purchase a phone number for an agent."""
    payload = {
        "agent_id": agent_id,
        "country": "US"  # Assuming we're purchasing a US number
    }
    
    response = requests.post(f"{RETELL_BASE_URL}/phone-numbers", headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error purchasing phone number: {response.text}")
        return None 