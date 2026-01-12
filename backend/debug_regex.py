#!/usr/bin/env python3
"""
Debug regex pattern matching
"""
import re

# Test content from the conversation
test_responses = [
    '"ఇన్విక్టస్" అనేది నేల ద్వారా సంక్రమించే వ్యాధులను నియంత్రించడానికి ఉపయోగించే ఒక ఉత్పత్తి. ఒక ఎకరానికి 10 కిలోల ఇన్విక్టస్ ను వాడాలి.',
    "ఎన్-ఫాక్టర్ మోతాదు ఎకరానికి 1 లీటరు.",
    "పి-ఫాక్టర్‌కు గరిష్ట మోతాదు ఎకరానికి 1 లీటరు."
]

product_info = [
    ("invictus", ["invictus", "ఇన్విక్టస్"]),
    ("n-factor", ["n-factor", "nfactor", "ఎన్-ఫాక్టర్"]),
    ("p-factor", ["p-factor", "pfactor", "పీ-ఫాక్టర్"])
]

print("Testing regex patterns on actual responses:\n")

for product_name, variants in product_info:
    print(f"Product: {product_name}")
    
    for response in test_responses:
        response_lower = response.lower()
        for variant in variants:
            # Original pattern
            pattern = rf'{re.escape(variant)}.*?(\d+(?:\.\d+)?)\s*(litre|liter|lt|kg|kilograms?|ml|gm|gram)'
            match = re.search(pattern, response_lower, re.IGNORECASE)
            
            if match:
                print(f"  ✅ Variant '{variant}' matched:")
                print(f"     Amount: {match.group(1)} {match.group(2)}")
            else:
                # Debug: show what's in the response
                if variant.lower() in response_lower:
                    print(f"  ℹ️  Variant '{variant}' found in text but dosage pattern didn't match")
                    # Show context
                    idx = response_lower.find(variant.lower())
                    if idx >= 0:
                        context = response_lower[idx:idx+100]
                        print(f"     Context: '{context}'")
    print()
