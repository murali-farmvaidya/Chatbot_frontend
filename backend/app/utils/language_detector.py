# app/utils/language_detector.py

import re

def detect_language(text: str) -> str:
    """
    Detect Indian language from text using Unicode ranges.
    Supports: Telugu, Tamil, Kannada, Malayalam, Hindi, Marathi, Bengali, Gujarati, Punjabi, Odia, English
    Returns: language code string
    """
    text = text.strip()
    
    # Count total characters (excluding spaces and punctuation)
    total_chars = len(re.findall(r'[^\s\W\d]', text))
    
    if total_chars == 0:
        return 'english'
    
    # Define language Unicode ranges
    languages = {
        'telugu': r'[\u0C00-\u0C7F]',      # తెలుగు
        'tamil': r'[\u0B80-\u0BFF]',       # தமிழ்
        'kannada': r'[\u0C80-\u0CFF]',     # ಕನ್ನಡ
        'malayalam': r'[\u0D00-\u0D7F]',   # മലയാളം
        'bengali': r'[\u0980-\u09FF]',     # বাংলা
        'gujarati': r'[\u0A80-\u0AFF]',    # ગુજરાતી
        'punjabi': r'[\u0A00-\u0A7F]',     # ਪੰਜਾਬੀ
        'odia': r'[\u0B00-\u0B7F]',        # ଓଡ଼ିଆ
        'hindi': r'[\u0900-\u097F]',       # हिंदी / मराठी (Devanagari script)
    }
    
    # Check each language (30% threshold)
    for lang, pattern in languages.items():
        lang_chars = len(re.findall(pattern, text))
        if lang_chars / total_chars > 0.3:
            return lang
    
    return 'english'


def get_language_instruction(language: str) -> str:
    """
    Get instruction to append to prompt for language-specific responses
    """
    instructions = {
        'telugu': "\n\nIMPORTANT: Respond ONLY in Telugu (తెలుగు) language. Do not use English.",
        'tamil': "\n\nIMPORTANT: Respond ONLY in Tamil (தமிழ்) language. Do not use English.",
        'kannada': "\n\nIMPORTANT: Respond ONLY in Kannada (ಕನ್ನಡ) language. Do not use English.",
        'malayalam': "\n\nIMPORTANT: Respond ONLY in Malayalam (മലയാളം) language. Do not use English.",
        'hindi': "\n\nIMPORTANT: Respond ONLY in Hindi (हिंदी) language. Do not use English.",
        'marathi': "\n\nIMPORTANT: Respond ONLY in Marathi (मराठी) language. Do not use English.",
        'bengali': "\n\nIMPORTANT: Respond ONLY in Bengali (বাংলা) language. Do not use English.",
        'gujarati': "\n\nIMPORTANT: Respond ONLY in Gujarati (ગુજરાતી) language. Do not use English.",
        'punjabi': "\n\nIMPORTANT: Respond ONLY in Punjabi (ਪੰਜਾਬੀ) language. Do not use English.",
        'odia': "\n\nIMPORTANT: Respond ONLY in Odia (ଓଡ଼ିଆ) language. Do not use English.",
        'english': "\n\nIMPORTANT: Respond ONLY in English language."
    }
    
    return instructions.get(language, instructions['english'])
