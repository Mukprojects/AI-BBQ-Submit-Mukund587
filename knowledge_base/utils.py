"""
Knowledge Base Utilities

This module contains utility functions for the knowledge base API,
including token counting and chunking responses to keep them under
the 800 token limit.
"""

import os
import json
import tiktoken
from typing import Dict, List, Any, Union, Optional

# Load environment variables
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "800"))

# Initialize tokenizer
tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    """Count the number of tokens in a text string."""
    return len(tokenizer.encode(text))

def truncate_to_token_limit(text: str, max_tokens: int = MAX_TOKENS) -> str:
    """Truncate a text to fit within the token limit."""
    tokens = tokenizer.encode(text)
    if len(tokens) <= max_tokens:
        return text
    
    truncated_tokens = tokens[:max_tokens-3] + tokenizer.encode("...")
    return tokenizer.decode(truncated_tokens)

def format_json_response(data: Any, max_tokens: int = MAX_TOKENS) -> str:
    """Format JSON data as a string, ensuring it's under the token limit."""
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    if count_tokens(json_str) <= max_tokens:
        return json_str
    
    # For complex objects, we need a smarter truncation strategy
    if isinstance(data, dict):
        return truncate_dict(data, max_tokens)
    elif isinstance(data, list):
        return truncate_list(data, max_tokens)
    else:
        return truncate_to_token_limit(json_str, max_tokens)

def truncate_dict(data: Dict, max_tokens: int = MAX_TOKENS) -> str:
    """Truncate a dictionary to fit within the token limit."""
    result = {}
    remaining_tokens = max_tokens
    
    # First pass: add keys until we hit the limit
    for key, value in data.items():
        value_str = json.dumps(value, ensure_ascii=False)
        key_and_value = f'"{key}": {value_str}'
        tokens_needed = count_tokens(key_and_value)
        
        if tokens_needed < remaining_tokens:
            result[key] = value
            remaining_tokens -= tokens_needed
        else:
            # If it's a complex value, try to truncate it
            if isinstance(value, dict) or isinstance(value, list):
                # For nested structures, we recursively truncate
                if isinstance(value, dict):
                    truncated_value = json.loads(truncate_dict(value, remaining_tokens - count_tokens(f'"{key}": ')))
                else:
                    truncated_value = json.loads(truncate_list(value, remaining_tokens - count_tokens(f'"{key}": ')))
                result[key] = truncated_value
                break
            else:
                # For simple values, we just skip if too large
                continue
    
    # Convert back to JSON string
    return json.dumps(result, ensure_ascii=False, indent=2)

def truncate_list(data: List, max_tokens: int = MAX_TOKENS) -> str:
    """Truncate a list to fit within the token limit."""
    result = []
    remaining_tokens = max_tokens
    
    # Add items until we hit the limit
    for item in data:
        item_str = json.dumps(item, ensure_ascii=False)
        tokens_needed = count_tokens(item_str) + 2  # +2 for comma and space
        
        if tokens_needed < remaining_tokens:
            result.append(item)
            remaining_tokens -= tokens_needed
        else:
            # For complex items, try to truncate
            if isinstance(item, dict) or isinstance(item, list):
                if isinstance(item, dict):
                    truncated_item = json.loads(truncate_dict(item, remaining_tokens - 2))
                else:
                    truncated_item = json.loads(truncate_list(item, remaining_tokens - 2))
                result.append(truncated_item)
                break
            else:
                # Indicate truncation
                result.append("...")
                break
    
    # Convert back to JSON string
    return json.dumps(result, ensure_ascii=False, indent=2)

def format_menu_response(menu_data: Dict, category: Optional[str] = None) -> Dict:
    """Format menu data for API response with token limiting."""
    
    if category and category in menu_data:
        # Return just the requested category
        return {
            "menu_category": category,
            "items": menu_data[category]
        }
    
    # Return a summary of all categories
    return {
        "categories": list(menu_data.keys()),
        "sample_items": {
            cat: items[:2] + (["..."] if len(items) > 2 else []) 
            for cat, items in menu_data.items()
        }
    }

def format_outlet_response(outlet_data: Dict, info_type: Optional[str] = None) -> Dict:
    """Format outlet data for API response with token limiting."""
    
    if info_type and info_type in outlet_data:
        # Return just the requested information type
        return {
            "info_type": info_type,
            "details": outlet_data[info_type]
        }
    
    # Return a summary
    return {
        "address": outlet_data.get("address", ""),
        "facilities_summary": f"{len(outlet_data.get('facilities', []))} facilities available",
        "hours_summary": "Open for lunch and dinner daily",
        "available_info": list(outlet_data.keys())
    } 