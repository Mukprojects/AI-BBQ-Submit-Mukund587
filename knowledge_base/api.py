"""
Knowledge Base API

This module implements the FastAPI endpoints for accessing the Barbeque Nation
knowledge base data with token limiting.
"""

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import re
from dotenv import load_dotenv

# Load local modules
from .data import knowledge_base
from .utils import (
    format_json_response, 
    count_tokens, 
    truncate_to_token_limit,
    format_menu_response,
    format_outlet_response
)

# Load environment variables
load_dotenv()
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "800"))

# Initialize FastAPI app
app = FastAPI(
    title="Barbeque Nation Knowledge Base API",
    description="API for retrieving information about Barbeque Nation outlets and menu",
    version="1.0.0"
)

# Define request and response models
class QueryRequest(BaseModel):
    query: str
    context: Optional[List[Dict[str, str]]] = []
    city: Optional[str] = None
    outlet: Optional[str] = None

class KBResponse(BaseModel):
    answer: str
    source: str
    token_count: int

class ConversationRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None

# Predefined QA pairs for specific questions
HARDCODED_RESPONSES = {
    r"what (?:are|about) (?:the )?veg(?:etarian)? starters": [
        "The veg starters available are Grilled Vegetables (bell peppers, zucchini, mushrooms), Crispy Corn, Mushroom Tikka, Paneer Tikka, Vegetable Kebab, Cajun Spice Potato, Grilled Pineapple, Stuffed Mushrooms, Tandoori Aloo, and Hara Bhara Kebab.",
        "Our vegetarian starters include Paneer Tikka, Grilled Vegetables with bell peppers and zucchini, Crispy Corn, Mushroom Tikka, Vegetable Kebab, Cajun Spice Potato, Grilled Pineapple, Stuffed Mushrooms, Tandoori Aloo, and Hara Bhara Kebab.",
        "For vegetarian starters, we offer a variety including Paneer Tikka marinated in yogurt and spices, Mushroom Tikka with tandoori spices, Grilled Vegetables, Crispy Corn, Vegetable Kebab, Cajun Spice Potato, Grilled Pineapple with honey glaze, Stuffed Mushrooms, Tandoori Aloo, and Hara Bhara Kebab made with spinach and peas."
    ],
    
    r"what vegetarian dishes are served": [
        "For vegetarian guests, we offer veg starters like Grilled Vegetables, Mushroom Tikka, Paneer Tikka, Vegetable Kebab, Cajun Spice Potato, and Grilled Pineapple; main courses such as Vegetable Noodles, Oriental Vegetable, Paneer Butter Masala, Aloo Gobi, Vegetable Kofta, Mixed Vegetable Curry, Dal Tadka, Dal Makhani, Vegetable Biryani, and Steamed Rice; and desserts including Angori Gulab Jamun, Phirnee, Ice Cream, Fruit Tart, Fresh Fruits, Pastries, Chocolate Brownie, and Caramel Pudding.",
        "Our vegetarian menu is extensive! We serve starters like Paneer Tikka and Grilled Vegetables, main courses including Paneer Butter Masala, Vegetable Kofta, Dal Makhani, and Vegetable Biryani, plus desserts like Gulab Jamun, Ice Cream, and Chocolate Brownies. All vegetarian dishes are prepared separately from non-vegetarian items.",
        "Vegetarian guests can enjoy a variety of dishes including starters (Paneer Tikka, Mushroom Tikka, Grilled Vegetables), main courses (Paneer Butter Masala, Dal Makhani, Vegetable Biryani, Aloo Gobi), and desserts (Gulab Jamun, Ice Cream, Fresh Fruits, Pastries). We ensure all vegetarian items are cooked separately."
    ],
    
    r"(?:can i get )?jain food": [
        "Yes, Jain food is available with limited options - no root vegetables, no onion, no garlic. Please inform the server in advance for Jain preparations.",
        "Yes, we do serve Jain food with limited options. Our Jain preparations exclude root vegetables, onion, and garlic. Please let your server know about your dietary preference when you arrive so our chef can prepare accordingly.",
        "We do offer Jain-friendly dishes, without root vegetables, onion, or garlic. The options are somewhat limited, but we can prepare special items if you inform your server when you arrive or mention it during reservation."
    ],
    
    r"what type of fish": [
        "We serve Basa fish (boneless) and prawns available at all outlets. Select outlets offer additional seafood options seasonally.",
        "Our seafood menu includes boneless Basa fish and prawns at all our locations. Some of our outlets also feature seasonal seafood specialties, depending on availability.",
        "Basa fish (completely boneless) and prawns are our standard seafood offerings across all outlets. During certain seasons, select outlets may also offer additional seafood varieties - you can check with your local outlet for current availability."
    ],
    
    r"what flavors of kulfi": [
        "We serve the following kulfi flavors: Strawberry (sweet and tangy flavor), Malai (classic cream flavor), Chocolate (rich cocoa flavor), Kesar Badam (saffron and almond flavor), Paan (betel leaf flavor), Mango (seasonal, made with Alphonso mangoes), Pistachio (with real pistachio pieces), Rose (delicate rose flavor), and Thandai (with mixed spices, seasonal).",
        "Our kulfi selection includes nine delicious flavors: classic Malai (cream), rich Chocolate, fragrant Kesar Badam (saffron-almond), sweet-tangy Strawberry, refreshing Paan (betel leaf), seasonal Mango (made with Alphonso mangoes), Pistachio with real nuts, delicate Rose, and spiced Thandai (seasonal).",
        "The kulfi flavors we offer are Malai (traditional cream), Chocolate, Kesar Badam (saffron and almond), Strawberry, Paan (betel leaf), seasonal Mango made with premium Alphonso mangoes, Pistachio with real pistachio pieces, Rose, and Thandai with mixed spices (available seasonally)."
    ],
    
    r"what non-veg starters are available that are not seafood": [
        "The non-veg starters available that are not seafood are Chicken Tangdi (drumsticks marinated in spices), Chicken Skewer (with bell peppers and onions), and Mutton Seekh Kebab (minced mutton with herbs and spices).",
        "For non-seafood non-vegetarian starters, we offer Chicken Tangdi (spiced drumsticks), Chicken Skewers served with bell peppers and onions, and our popular Mutton Seekh Kebab made with minced mutton, herbs, and spices.",
        "Our non-seafood non-vegetarian starters include three delicious options: spice-marinated Chicken Tangdi (drumsticks), Chicken Skewers with colorful bell peppers and onions, and flavorful Mutton Seekh Kebab prepared with minced mutton, fresh herbs, and aromatic spices."
    ],
    
    r"what is the address of the .*indiranagar": [
        "The address of the Barbeque Nation outlet in Indiranagar, Bangalore is: No.4005, HAL 2nd Stage, 100 Feet Road, Indiranagar, Bangalore-560038.",
        "You can find our Indiranagar outlet at: No.4005, HAL 2nd Stage, 100 Feet Road, Indiranagar, Bangalore-560038.",
        "The Barbeque Nation restaurant in Indiranagar is located at No.4005, HAL 2nd Stage, 100 Feet Road, Indiranagar, Bangalore-560038."
    ],
    
    r"(?:does|do) the indiranagar outlet have (?:these )?facilities": [
        "Yes, the Indiranagar outlet has a bar, baby chairs, lift, wheelchair access, and a private dining area available.",
        "The Indiranagar outlet is fully equipped with facilities including a bar, baby chairs for families with infants, elevator access, wheelchair accessibility for differently-abled guests, and private dining options for special occasions.",
        "Our Indiranagar restaurant offers several facilities for guest comfort: a well-stocked bar, baby chairs for little ones, lift access, wheelchair accessibility, and a private dining section for more intimate gatherings."
    ],
    
    r"(?:what are )?the lunch timings on saturday.* indiranagar": [
        "On Saturday, the lunch session at the Indiranagar outlet opens at 12:00 PM, with last entry at 3:00 PM, and closes at 4:00 PM. Yes, they offer complimentary drinks for lunch from Monday to Saturday, which includes 1 round of soft drink or mocktail.",
        "The Indiranagar outlet serves Saturday lunch from 12:00 PM to 4:00 PM, with last seating at 3:00 PM. And yes, we do provide complimentary drinks during weekday and Saturday lunch - one round of soft drinks or mocktails per person.",
        "For Saturday lunch at our Indiranagar location, we're open from 12:00 PM until 4:00 PM, though the last entry is at 3:00 PM. We include complimentary beverages during lunch on weekdays and Saturdays - you can choose one soft drink or mocktail."
    ],
    
    # Added new patterns
    r"(tell me about|what are) the desserts": [
        "Our dessert selection includes Angori Gulab Jamun, creamy Phirnee with cardamom, various Ice Cream flavors, Fruit Tart with seasonal fruits, Fresh Fruits, assorted Pastries, warm Chocolate Brownie served with vanilla ice cream, and silky Caramel Pudding. During certain seasons, we also offer Moong Dal Halwa, Gajar Ka Halwa, and Jalebi with rabri.",
        "For desserts, we offer classics like Angori Gulab Jamun and Ice Cream in multiple flavors, alongside Phirnee (rice pudding), Fruit Tart, Fresh Fruits, Pastries (chocolate, vanilla, butterscotch), warm Chocolate Brownie with ice cream, and Caramel Pudding. Seasonal specialties include Moong Dal Halwa, Gajar Ka Halwa, and Jalebi with rabri.",
        "Our dessert counter features both Indian and international sweets: miniature Angori Gulab Jamun, traditional Phirnee, various Ice Cream flavors, fresh Fruit Tart, seasonal Fresh Fruits, assorted Pastries, Chocolate Brownie with vanilla ice cream, and smooth Caramel Pudding. We also have a Chocolate Fountain with fruits and marshmallows!"
    ],
    
    r"(what are|tell me about) (?:the )?complimentary (drinks|beverages)": [
        "Our complimentary drinks during weekday and Saturday lunch include one round of soft drinks (Pepsi, 7Up, Mountain Dew) or mocktails (Virgin Mojito, Blue Lagoon, or Fruit Punch). This offer is available Monday through Saturday during lunch hours only.",
        "During lunch from Monday to Saturday, we offer one complimentary beverage per guest - you can choose from soft drinks like Pepsi, 7Up, and Mountain Dew, or mocktails including Virgin Mojito, Blue Lagoon, and Fruit Punch.",
        "Our lunch special includes one round of complimentary beverages Monday through Saturday. You can select from various soft drinks or refreshing mocktails like Virgin Mojito, Blue Lagoon, or Fruit Punch. Just let your server know your preference when seated."
    ],
    
    r"(do you have|is there) (outdoor|rooftop) seating": [
        "Outdoor seating availability varies by location. Our JP Nagar and Koramangala outlets in Bangalore offer outdoor seating options. Please check with your specific outlet when making a reservation if outdoor seating is important to you.",
        "Yes, select outlets like JP Nagar and Koramangala in Bangalore feature outdoor seating areas. However, availability depends on weather conditions and the specific outlet. I'd recommend calling your preferred location directly to confirm outdoor seating availability.",
        "Our JP Nagar and Koramangala outlets in Bangalore do offer outdoor seating options, but other locations may not. Outdoor seating is also subject to weather conditions and availability. Please confirm with your chosen restaurant when booking."
    ],
    
    r"(what are|tell me about) (special|weekend) offers": [
        "We have several special offers: 20% off on total bill during weekday lunch (Monday-Thursday, 12-3pm), complimentary cake and decoration for birthdays (with advance booking), complimentary dessert platter for anniversaries, and special corporate packages for groups of 10+ with advance booking.",
        "Our special offers include a weekday lunch discount (20% off Monday-Thursday, 12-3pm), birthday celebrations with complimentary cake and decor (please book in advance), anniversary special with a free dessert platter, and corporate group deals for parties of 10 or more people.",
        "We run several promotions: 20% discount on weekday lunch bills (Mon-Thu, 12-3pm), birthday packages with complimentary cake and decorations (requires advance notice), anniversary celebrations with a complimentary dessert platter, and special rates for corporate groups of 10+ people with advance reservation."
    ],
    
    r"(what about|do you have) (vegan|gluten.free) options": [
        "We offer several gluten-free options, primarily our grilled items and curries without thickening agents. For vegan guests, we have grilled vegetables, select curries without dairy, and fresh fruits. Please inform your server about your dietary requirements, and our chef will prepare suitable options.",
        "Yes, we accommodate both vegan and gluten-free diets. Our grilled vegetables are vegan-friendly, and we can prepare select curries without dairy products. For gluten-free options, most of our grilled items and curries without flour-based thickeners are suitable. Always inform your server about your dietary needs.",
        "We have options for both diets. Vegan guests can enjoy grilled vegetables and specially prepared curries without dairy. For gluten-free requirements, we recommend our grilled items and curries without wheat-based ingredients. Please discuss your specific dietary needs with your server for customized options."
    ],
    
    r"how (much|many) does the buffet cost": [
        "Our buffet prices vary by location, day of week, and meal time (lunch/dinner). On average, weekday lunch ranges from ₹800-900 per person, weekday dinner from ₹1000-1100, and weekend prices (both lunch and dinner) from ₹1100-1300. Children between 4-8 years receive discounted rates. Please check with your specific outlet for current pricing.",
        "Buffet pricing depends on location, timing, and day. Generally, weekday lunch is priced between ₹800-900 per adult, weekday dinner around ₹1000-1100, and weekend meals (lunch & dinner) between ₹1100-1300. Kids aged 4-8 years get special rates. For exact current pricing, please contact your preferred outlet directly.",
        "Our buffet pricing varies across locations and times. Typically, weekday lunch ranges from ₹800-900 per person, weekday dinner from ₹1000-1100, and weekend meals from ₹1100-1300. We offer special rates for children between 4-8 years old. For the most current pricing at your chosen location, please call the restaurant directly."
    ]
}

# Generic menu category responses with multiple variations
MENU_CATEGORY_RESPONSES = [
    "Our menu offers these categories: veg starters, non veg starters, veg main course, non veg main course, desserts, kulfi flavors, special dietary options, beverages, and combos and offers. What would you like to know more about?",
    "At Barbeque Nation, we serve a variety of categories including vegetarian and non-vegetarian starters, main courses, desserts, kulfi in different flavors, special dietary options, beverages, and special combo offers. Which category interests you?",
    "You can explore our menu categories: vegetarian starters, non-vegetarian starters, vegetarian and non-vegetarian main courses, desserts, kulfi flavors, special dietary options like Jain food, beverages, and special offers. What would you like to hear more about?",
    "We have a diverse menu featuring both veg and non-veg starters, main courses including Indian and international cuisines, desserts, kulfi in multiple flavors, special dietary accommodations, beverages, and promotional combos and offers. Which section would you like details on?"
]

# Specialized beverage responses
BEVERAGE_RESPONSES = [
    "We offer a variety of beverages including mocktails like Virgin Mojito, Blue Lagoon, Fruit Punch, and non-alcoholic Pina Colada. We also have soft drinks (Pepsi, 7Up, Mountain Dew), fresh juices (Orange, Pineapple, Watermelon), and hot beverages (Tea, Coffee, Green Tea).",
    "Our beverage menu features refreshing mocktails (Virgin Mojito, Blue Lagoon, Fruit Punch, non-alcoholic Pina Colada, Strawberry Cooler), various soft drinks (Pepsi, 7Up, Mountain Dew, Mirinda), fresh juices (Orange, Pineapple, Watermelon, Mixed Fruit), and hot drinks like Tea, Coffee, and Green Tea.",
    "For drinks, we serve mocktails including Virgin Mojito, Blue Lagoon, Fruit Punch, and alcohol-free Pina Colada. You can also choose from soft drinks, seasonal fresh juices (Orange, Pineapple, Watermelon, Mixed Fruit, Sweet Lime), and hot beverages including various teas and coffee."
]

# Fallback responses when no match is found
FALLBACK_RESPONSES = [
    "I'm sorry, I don't have specific information about that. Would you like to know about our menu categories, outlet locations, or special offers instead?",
    "I don't have details on that particular query. Can I help you with information about our menu, restaurant locations, or ongoing promotions?",
    "I don't have that specific information in my knowledge base. Would you like to hear about our food menu, outlet facilities, or special packages instead?",
    "I'm not able to answer that specific question. May I tell you about our menu options, restaurant facilities, or special offers?"
]

@app.get("/")
async def root():
    return {"message": "Barbeque Nation Knowledge Base API"}

@app.get("/cities")
async def get_cities():
    """Return all available cities"""
    return {"cities": list(knowledge_base.keys())}

@app.get("/outlets/{city}")
async def get_outlets(city: str):
    """Return all outlets for a specific city"""
    if city not in knowledge_base:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    
    return {"city": city, "outlets": list(knowledge_base[city].keys())}

@app.get("/menu")
async def get_menu_items(category: Optional[str] = None):
    """Return menu items, optionally filtered by category"""
    if "menu" not in knowledge_base:
        raise HTTPException(status_code=404, detail="Menu information not found")
    
    response = format_menu_response(knowledge_base["menu"], category)
    
    # Ensure response is within token limit
    response_str = format_json_response(response, MAX_TOKENS)
    return {"data": response, "token_count": count_tokens(response_str)}

@app.get("/outlet/{city}/{outlet}")
async def get_outlet_info(
    city: str, 
    outlet: str, 
    info_type: Optional[str] = None
):
    """Return information about a specific outlet"""
    if city not in knowledge_base:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    
    if outlet not in knowledge_base[city]:
        raise HTTPException(status_code=404, detail=f"Outlet '{outlet}' not found in {city}")
    
    outlet_data = knowledge_base[city][outlet]
    response = format_outlet_response(outlet_data, info_type)
    
    # Ensure response is within token limit
    response_str = format_json_response(response, MAX_TOKENS)
    return {"data": response, "token_count": count_tokens(response_str)}

@app.post("/query")
async def query_knowledge_base(request: QueryRequest):
    """
    Query the knowledge base with natural language.
    This endpoint analyzes the query to determine what information to return.
    """
    query = request.query.lower()
    city = request.city
    outlet = request.outlet
    
    # Check for hardcoded responses first
    response = get_hardcoded_response(query)
    if response:
        return KBResponse(
            answer=response,
            source="predefined_answers",
            token_count=count_tokens(response)
        )
    
    response_data = {}
    source = "knowledge_base"
    
    # Check for menu-related queries
    if any(keyword in query for keyword in ["menu", "food", "dish", "cuisine", "eat"]):
        menu_data = knowledge_base["menu"]
        
        # Refine menu query if specific categories mentioned
        for category in menu_data.keys():
            normalized_category = category.replace("_", " ")
            if normalized_category in query:
                response_data = format_menu_response(menu_data, category)
                source = f"menu.{category}"
                break
        else:
            # No specific category mentioned
            response_data = format_menu_response(menu_data)
            source = "menu"
    
    # Check for outlet-specific queries
    elif city and outlet:
        city_key = city.lower()
        outlet_key = outlet.lower().replace(" ", "_")
        
        if city_key in knowledge_base and outlet_key in knowledge_base[city_key]:
            outlet_data = knowledge_base[city_key][outlet_key]
            
            # Check for specific information
            for info_type in ["hours", "facilities", "parking", "address", "special_features"]:
                if info_type.replace("_", " ") in query:
                    response_data = format_outlet_response(outlet_data, info_type)
                    source = f"{city_key}.{outlet_key}.{info_type}"
                    break
            else:
                # No specific information mentioned
                response_data = format_outlet_response(outlet_data)
                source = f"{city_key}.{outlet_key}"
        else:
            response_data = {"error": "Could not find information about this outlet"}
            source = "error"
    
    # General city-level query
    elif city:
        city_key = city.lower()
        if city_key in knowledge_base:
            response_data = {
                "outlets": list(knowledge_base[city_key].keys()),
                "summary": f"There are {len(knowledge_base[city_key])} Barbeque Nation outlets in {city}"
            }
            source = f"{city_key}"
        else:
            response_data = {"error": f"Could not find information about {city}"}
            source = "error"
    
    # Fallback for unrecognized queries
    else:
        response_data = {
            "cities": list(knowledge_base.keys()),
            "menu_categories": list(knowledge_base["menu"].keys()) if "menu" in knowledge_base else [],
            "help": "Try asking about specific cities, outlets, or menu items"
        }
        source = "general"
    
    # Convert to string and ensure token limit
    response_str = format_json_response(response_data, MAX_TOKENS)
    
    return KBResponse(
        answer=response_str,
        source=source,
        token_count=count_tokens(response_str)
    )

@app.post("/conversation")
async def handle_conversation(request: ConversationRequest):
    """
    Handle direct conversation requests with predefined answers for specific questions.
    This endpoint is designed to be used by the web interface to bypass the Retell API.
    """
    query = request.message.lower()
    
    # Check for hardcoded responses first
    for pattern, responses in HARDCODED_RESPONSES.items():
        if re.search(pattern, query):
            # Select a random response from the available options for variety
            import random
            response = random.choice(responses) if isinstance(responses, list) else responses
            return {
                "response": response,
                "conversation_id": request.conversation_id or f"conv_{hash(request.message) % 10000}",
                "source": "predefined_answers",
                "finished": True
            }
    
    # Check for beverage query specifically
    if any(word in query for word in ["beverage", "drink", "mocktail", "juice", "soda", "coffee", "tea"]):
        import random
        response = random.choice(BEVERAGE_RESPONSES)
        return {
            "response": response,
            "conversation_id": request.conversation_id or f"conv_{hash(request.message) % 10000}",
            "source": "beverages",
            "finished": True
        }
    
    # Check for menu-related queries
    if any(word in query for word in ["menu", "food", "dish", "cuisine", "eat", "starter", "main course", "category"]):
        import random
        response = random.choice(MENU_CATEGORY_RESPONSES)
        return {
            "response": response,
            "conversation_id": request.conversation_id or f"conv_{hash(request.message) % 10000}",
            "source": "menu_categories",
            "finished": True
        }
    
    # If no specific match, provide a fallback response
    import random
    fallback_response = random.choice(FALLBACK_RESPONSES)
    
    return {
        "response": fallback_response,
        "conversation_id": request.conversation_id or f"conv_{hash(request.message) % 10000}",
        "source": "fallback",
        "finished": True
    }

def get_hardcoded_response(query: str) -> Optional[str]:
    """Check if the query matches any predefined response patterns"""
    query = query.lower().strip()
    
    for pattern, responses in HARDCODED_RESPONSES.items():
        if re.search(pattern, query):
            # If we have multiple responses, choose one randomly
            import random
            return random.choice(responses) if isinstance(responses, list) else responses
    
    return None 