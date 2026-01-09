#!/usr/bin/env python3
"""
Debug pattern matching more carefully
"""
import re

responses = {
    "invictus": '"ఇన్విక్టస్" అనేది నేల ద్వారా సంక్రమించే వ్యాధులను నియంత్రించడానికి ఉపయోగించే ఒక ఉత్పత్తి. ఒక ఎకరానికి 10 కిలోల ఇన్విక్టస్ ను వాడాలి.',
    "n-factor": "ఎన్-ఫాక్టర్ మోతాదు ఎకరానికి 1 లీటరు.",
    "p-factor": "పి-ఫాక్టర్‌కు గరిష్ట మోతాదు ఎకరానికి 1 లీటరు."
}

# Units
unit_patterns = [
    "litre", "liter", "lt", "लीटर", "లీటర్", "ली",
    "kg", "kilo", "किलोग्राम", "కిలోగ్రాम్", "क.ग्रा",
    "ml", "mili", "मिली", "మిల్లీ",
    "gm", "gram", "ग्राम", "గ్రాం"
]

for product, response in responses.items():
    print(f"\n{'='*60}")
    print(f"Product: {product}")
    print(f"Response: {response[:80]}...")
    print(f"{'='*60}")
    
    # Check if numbers exist
    numbers = re.findall(r'\d+', response)
    print(f"Numbers found: {numbers}")
    
    # Check if units exist  
    for unit in unit_patterns:
        if unit in response.lower():
            print(f"✓ Unit '{unit}' found in response")
    
    # Try pattern
    units_pattern = "|".join(unit_patterns)
    pattern = rf'(\d+(?:\.\d+)?)\s*({units_pattern})'
    matches = re.findall(pattern, response, re.IGNORECASE)
    print(f"\nPattern matches: {matches}")
    
    # Find numbers before units
    # Maybe the unit is separate
    print(f"\nDebug: Looking for 'కిలోగ్రాम్' or 'కిలో'...")
    if 'కిలో' in response:
        print("  Found 'కిలో'")
    if 'కిలోల' in response:
        print("  Found 'కిలోల'")
    if 'లీటర' in response:
        print("  Found 'లీటర'")
