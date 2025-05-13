"""
Knowledge Base Data

This file contains the structured data for Barbeque Nation outlets in Bangalore and Delhi,
along with menu information extracted from the PDF files.
"""

knowledge_base = {
    "bangalore": {
        "indiranagar": {
            "address": "No.4005, HAL 2nd Stage, 100 Feet Road, Indiranagar, Bangalore-560038",
            "contact": "+91 80-4411-4100",
            "hours": {
                "weekday": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"},
                "weekend": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"}
            },
            "facilities": ["Bar", "Baby Chairs", "Lift", "Wheelchair Access", "Private Dining Area"],
            "parking": "Valet Parking Available",
            "special_features": ["Complimentary drinks during lunch (Mon-Sat): 1 round of soft drink or mocktail", "Live music on weekends"]
        },
        "jp_nagar": {
            "address": "67, 3rd Floor, 6th B Main, Phase III, J P Nagar, Bengaluru, Karnataka 560078, India",
            "contact": "+91 80-4155-3344",
            "hours": {
                "weekday": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"},
                "weekend": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"}
            },
            "facilities": ["Bar", "Baby Chairs", "Lift", "Wheelchair Access", "Outdoor Seating"],
            "parking": "Valet Parking Available",
            "special_features": ["Located on 3rd floor which offers quieter dining experience", "Complimentary drinks during lunch (Mon-Sat): 1 round of soft drink or mocktail"]
        },
        "electronic_city": {
            "address": "Survey No.8/5, Neeladri Road, Electronics City Phase 1, Bengaluru, Karnataka 560100, India",
            "contact": "+91 80-4115-1234",
            "hours": {
                "weekday": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"},
                "weekend": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"}
            },
            "facilities": ["Bar", "Baby Chairs", "Lift", "Wheelchair Access", "Free Wi-Fi"],
            "parking": "Free Parking Available",
            "special_features": ["Convenient location for IT professionals", "Complimentary drinks during lunch (Mon-Sat): 1 round of soft drink or mocktail", "Special corporate packages available"]
        },
        "koramangala": {
            "address": "No. 120, Industrial Layout, Koramangala, Bengaluru, Karnataka 560095, India",
            "contact": "+91 80-4112-6060",
            "hours": {
                "weekday": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"},
                "weekend": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"}
            },
            "facilities": ["Bar", "Baby Chairs", "Lift", "Private Dining", "Outdoor Seating"],
            "parking": "Valet Parking Available",
            "special_features": ["Popular among young professionals", "Complimentary drinks during lunch (Mon-Sat): 1 round of soft drink or mocktail", "Trendy ambiance with modern decor"]
        },
        "whitefield": {
            "address": "Phoenix Marketcity, Whitefield Main Road, Mahadevapura, Bengaluru, Karnataka 560048, India",
            "contact": "+91 80-4909-0909",
            "hours": {
                "weekday": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"},
                "weekend": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"}
            },
            "facilities": ["Bar", "Baby Chairs", "Lift", "Wheelchair Access", "Mall Access"],
            "parking": "Mall Parking Available",
            "special_features": ["Located in Phoenix Marketcity mall", "Complimentary drinks during lunch (Mon-Sat): 1 round of soft drink or mocktail", "Special weekend buffet options"]
        }
    },
    "delhi": {
        "connaught_place": {
            "address": "N-12, Outer Circle, Connaught Place, New Delhi, Delhi 110001, India",
            "contact": "+91 11-4218-8822",
            "hours": {
                "weekday": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"},
                "weekend": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"}
            },
            "facilities": ["Bar", "Baby Chairs", "Lift", "Outdoor Seating"],
            "parking": "Paid Parking Nearby",
            "special_features": ["Located in the heart of Delhi", "Complimentary drinks during lunch (Mon-Sat): 1 round of soft drink or mocktail", "Historic location with modern amenities"]
        },
        "vasant_kunj": {
            "address": "Ambience Mall, 2nd Floor, Plot No.2, Nelson Mandela Road, Vasant Kunj, New Delhi, Delhi 110070, India",
            "contact": "+91 11-4087-0800",
            "hours": {
                "weekday": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"},
                "weekend": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"}
            },
            "facilities": ["Bar", "Baby Chairs", "Lift", "Wheelchair Access", "Mall Access"],
            "parking": "Mall Parking Available",
            "special_features": ["Located in premium Ambience Mall", "Complimentary drinks during lunch (Mon-Sat): 1 round of soft drink or mocktail", "Luxury dining experience"]
        },
        "janakpuri": {
            "address": "3rd Floor, Unity One Mall, Janakpuri, New Delhi, Delhi 110058, India",
            "contact": "+91 11-4580-1234",
            "hours": {
                "weekday": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"},
                "weekend": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"}
            },
            "facilities": ["Bar", "Baby Chairs", "Lift", "Family Seating"],
            "parking": "Mall Parking Available",
            "special_features": ["Located in Unity Mall", "Complimentary drinks during lunch (Mon-Sat): 1 round of soft drink or mocktail", "Family-friendly atmosphere"]
        },
        "saket": {
            "address": "Select Citywalk Mall, A-3, District Centre, Saket, New Delhi, Delhi 110017, India",
            "contact": "+91 11-4051-9797",
            "hours": {
                "weekday": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"},
                "weekend": {"lunch": "12:00 PM - 4:00 PM (last entry 3:00 PM)", "dinner": "6:30 PM - 11:00 PM (last entry 10:00 PM)"}
            },
            "facilities": ["Bar", "Baby Chairs", "Lift", "Wheelchair Access", "Premium Seating"],
            "parking": "Mall Parking Available",
            "special_features": ["Located in upscale Select Citywalk Mall", "Complimentary drinks during lunch (Mon-Sat): 1 round of soft drink or mocktail", "Premium dining experience"]
        }
    },
    "menu": {
        "veg_starters": [
            "Grilled Vegetables (bell peppers, zucchini, mushrooms)",
            "Crispy Corn",
            "Mushroom Tikka (marinated in tandoori spices)",
            "Paneer Tikka (cottage cheese marinated in yogurt and spices)",
            "Vegetable Kebab (mixed vegetable patties with herbs)",
            "Cajun Spice Potato (baby potatoes with Cajun seasoning)",
            "Grilled Pineapple (with honey glaze)",
            "Stuffed Mushrooms (with cheese and herbs)",
            "Tandoori Aloo (spiced potatoes)",
            "Hara Bhara Kebab (spinach and pea patties)"
        ],
        "non_veg_starters": [
            "Chicken Tangdi (drumsticks marinated in spices)",
            "Chicken Tikka (boneless chicken with yogurt marinade)",
            "Chicken Skewers (with bell peppers and onions)",
            "Mutton Seekh Kebab (minced mutton with herbs and spices)",
            "Basa Fish Tikka (boneless fish with lemon and spices)",
            "Garlic Prawns (with butter and herbs)",
            "Chicken Wings (spicy BBQ flavor)",
            "Lemon Chicken (with citrus marinade)",
            "Tandoori Pomfret (when in season)",
            "Squid Rings (when available, at select outlets)"
        ],
        "veg_main_course": [
            "Vegetable Noodles (with soy sauce and vegetables)",
            "Oriental Vegetable (stir-fried in Asian sauce)",
            "Paneer Butter Masala (cottage cheese in tomato gravy)",
            "Aloo Gobi (potato and cauliflower curry)",
            "Vegetable Kofta (mixed vegetable dumplings in gravy)",
            "Mixed Vegetable Curry (seasonal vegetables in spices)",
            "Dal Tadka (yellow lentils with tempering)",
            "Dal Makhani (black lentils slow-cooked with cream)",
            "Vegetable Biryani (aromatic rice with vegetables)",
            "Steamed Rice (basmati rice)",
            "Assorted Indian Breads (naan, roti, kulcha)",
            "Vegetable Pulao (rice cooked with vegetables and spices)",
            "Palak Paneer (spinach and cottage cheese curry)",
            "Chana Masala (chickpea curry)"
        ],
        "non_veg_main_course": [
            "Chicken Biryani (aromatic rice with chicken pieces)",
            "Butter Chicken (tandoori chicken in creamy tomato gravy)",
            "Mutton Rogan Josh (slow-cooked mutton in Kashmiri spices)",
            "Fish Curry (local fish in coconut or tomato gravy)",
            "Egg Curry (boiled eggs in spiced gravy)",
            "Chicken Tikka Masala (grilled chicken in spiced gravy)",
            "Prawn Curry (with coconut base, at select outlets)",
            "Chicken Dum Biryani (slow-cooked chicken and rice)",
            "Mutton Keema (minced mutton with peas)",
            "Fish Masala (boneless fish in onion-tomato gravy)"
        ],
        "desserts": [
            "Angori Gulab Jamun (mini dumplings in sugar syrup)",
            "Phirnee (rice pudding with cardamom)",
            "Ice Cream (multiple flavors)",
            "Fruit Tart (seasonal fruits on pastry)",
            "Fresh Fruits (seasonal selection)",
            "Pastries (chocolate, vanilla, butterscotch)",
            "Chocolate Brownie (with vanilla ice cream)",
            "Caramel Pudding (with caramel sauce)",
            "Moong Dal Halwa (seasonal)",
            "Gajar Ka Halwa (seasonal)",
            "Kulfi (traditional Indian ice cream)",
            "Jalebi (with rabri, at select outlets)",
            "Chocolate Fountain (with fruits and marshmallows)"
        ],
        "kulfi_flavors": [
            "Strawberry (sweet and tangy flavor)",
            "Malai (classic cream flavor)",
            "Chocolate (rich cocoa flavor)",
            "Kesar Badam (saffron and almond flavor)",
            "Paan (betel leaf flavor)",
            "Mango (seasonal, made with Alphonso mangoes)",
            "Pistachio (with real pistachio pieces)",
            "Rose (delicate rose flavor)",
            "Thandai (with mixed spices, seasonal)"
        ],
        "special_dietary": {
            "jain_food": "Available with limited options - no root vegetables, no onion, no garlic. Please inform the server in advance for Jain preparations.",
            "seafood": "Basa fish (boneless) and prawns available at all outlets. Select outlets offer additional seafood options seasonally.",
            "gluten_free": "Several gluten-free options available including grilled items and curries. Please inform your server about allergies.",
            "low_calorie": "Specially marked low-calorie options include grilled vegetables, tandoori items without cream, and fresh fruit desserts."
        },
        "beverages": {
            "mocktails": ["Virgin Mojito", "Blue Lagoon", "Fruit Punch", "Pina Colada (non-alcoholic)", "Strawberry Cooler"],
            "soft_drinks": ["Pepsi", "7Up", "Mountain Dew", "Mirinda", "Soda Water"],
            "fresh_juices": ["Orange", "Pineapple", "Watermelon", "Mixed Fruit", "Sweet Lime"],
            "hot_beverages": ["Tea", "Coffee", "Green Tea", "Hot Chocolate"]
        },
        "combos_and_offers": {
            "weekday_lunch_special": "20% off on total bill (Monday to Thursday, 12pm to 3pm)",
            "birthday_celebration": "Complimentary cake and decoration with advance booking",
            "anniversary_special": "Complimentary dessert platter for the couple",
            "corporate_packages": "Special rates for groups of 10 or more with advance booking"
        }
    }
} 