"""
Conversation Flow Transitions

This module defines the transitions between states in the conversation flow.
Each transition has a source state, a destination state, and a condition.
"""

transitions = [
    # Greeting transitions
    {
        "source": "greeting",
        "destination": "city_collection",
        "condition": "user_response and not context.get('city')",
        "description": "Initial greeting to collecting city"
    },
    
    # City collection transitions
    {
        "source": "city_collection",
        "destination": "outlet_collection",
        "condition": "context.get('city')",
        "description": "City collected, now collect outlet"
    },
    {
        "source": "city_collection",
        "destination": "fallback",
        "condition": "attempt_count > 2 and not context.get('city')",
        "description": "Failed to collect city after multiple attempts"
    },
    
    # Outlet collection transitions
    {
        "source": "outlet_collection",
        "destination": "intent_identification",
        "condition": "context.get('city') and context.get('outlet')",
        "description": "City and outlet collected, now identify intent"
    },
    {
        "source": "outlet_collection",
        "destination": "fallback",
        "condition": "attempt_count > 2 and not context.get('outlet')",
        "description": "Failed to collect outlet after multiple attempts"
    },
    
    # Intent identification transitions
    {
        "source": "intent_identification",
        "destination": "information_inquiry",
        "condition": "context.get('intent') == 'inquiry'",
        "description": "Customer wants information"
    },
    {
        "source": "intent_identification",
        "destination": "new_reservation",
        "condition": "context.get('intent') == 'new_reservation'",
        "description": "Customer wants to make a reservation"
    },
    {
        "source": "intent_identification",
        "destination": "modify_reservation",
        "condition": "context.get('intent') == 'modify_reservation'",
        "description": "Customer wants to modify a reservation"
    },
    {
        "source": "intent_identification",
        "destination": "cancel_reservation",
        "condition": "context.get('intent') == 'cancel_reservation'",
        "description": "Customer wants to cancel a reservation"
    },
    {
        "source": "intent_identification",
        "destination": "fallback",
        "condition": "attempt_count > 2 and not context.get('intent')",
        "description": "Failed to identify intent after multiple attempts"
    },
    
    # Information inquiry transitions
    {
        "source": "information_inquiry",
        "destination": "farewell",
        "condition": "context.get('inquiry_complete') == True",
        "description": "Information provided, end conversation"
    },
    {
        "source": "information_inquiry",
        "destination": "intent_identification",
        "condition": "context.get('change_intent') == True",
        "description": "Customer wants to do something else after getting information"
    },
    
    # New reservation transitions
    {
        "source": "new_reservation",
        "destination": "reservation_confirmation",
        "condition": "context.get('date') and context.get('time') and context.get('party_size') and context.get('customer_name') and context.get('phone_number')",
        "description": "All reservation details collected, confirm reservation"
    },
    {
        "source": "new_reservation",
        "destination": "fallback",
        "condition": "attempt_count > 5 and not (context.get('date') and context.get('time') and context.get('party_size') and context.get('customer_name') and context.get('phone_number'))",
        "description": "Failed to collect all reservation details after multiple attempts"
    },
    
    # Reservation confirmation transitions
    {
        "source": "reservation_confirmation",
        "destination": "farewell",
        "condition": "context.get('reservation_confirmed') == True",
        "description": "Reservation confirmed, end conversation"
    },
    
    # Modify reservation transitions
    {
        "source": "modify_reservation",
        "destination": "farewell",
        "condition": "context.get('modification_complete') == True",
        "description": "Reservation modified, end conversation"
    },
    {
        "source": "modify_reservation",
        "destination": "fallback",
        "condition": "attempt_count > 5 and not context.get('modification_complete')",
        "description": "Failed to complete modification after multiple attempts"
    },
    
    # Cancel reservation transitions
    {
        "source": "cancel_reservation",
        "destination": "farewell",
        "condition": "context.get('cancellation_complete') == True",
        "description": "Reservation cancelled, end conversation"
    },
    {
        "source": "cancel_reservation",
        "destination": "fallback",
        "condition": "attempt_count > 3 and not context.get('cancellation_complete')",
        "description": "Failed to complete cancellation after multiple attempts"
    },
    
    # Fallback transitions
    {
        "source": "fallback",
        "destination": "city_collection",
        "condition": "context.get('restart') == True",
        "description": "Restart conversation from city collection"
    },
    {
        "source": "fallback",
        "destination": "farewell",
        "condition": "context.get('end_conversation') == True or attempt_count > 2",
        "description": "End conversation after multiple fallbacks"
    }
]

# Function to filter transitions by source state
def get_transitions_from_state(state_name):
    return [t for t in transitions if t["source"] == state_name]

# Function to get the next state based on current state and context
def get_next_state(current_state, context, attempt_count=0):
    # Get transitions from the current state
    possible_transitions = get_transitions_from_state(current_state)
    
    # Evaluate each transition condition
    for transition in possible_transitions:
        # In a real implementation, we would evaluate the condition string
        # For this simplified version, we'll directly check the context
        condition = transition["condition"]
        
        # Simple condition evaluation logic (would be more sophisticated in production)
        condition_met = False
        
        if "context.get('city')" in condition and context.get('city'):
            condition_met = True
        elif "context.get('outlet')" in condition and context.get('outlet'):
            condition_met = True
        elif "context.get('intent')" in condition and context.get('intent'):
            condition_met = True
        # Add more condition checks as needed
        
        if "attempt_count >" in condition:
            # Extract the attempt count threshold
            threshold = int(condition.split("attempt_count >")[1].split(" and")[0].strip())
            if attempt_count > threshold:
                condition_met = True
        
        if condition_met:
            return transition["destination"]
    
    # If no transition condition is met, stay in the current state
    return current_state 