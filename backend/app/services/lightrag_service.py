import requests
from app.core.config import LIGHTRAG_URL

def query_lightrag(query, history, mode="mix", language="english", factual=False):
    """
    Query LightRAG with language awareness
    
    Args:
        query: The user's question
        history: Conversation history
        mode: LightRAG mode (mix, local, global, bypass)
        language: Language to respond in (english, telugu, hindi, etc.)
        factual: If True, use softer language instruction to avoid forcing wrong answers
    """
    # Add language instruction to the query
    # For factual questions, use softer instructions to avoid forcing answers when no info exists
    if factual and language != "english":
        language_instructions = {
            "telugu": "\n\nNote: Please respond in Telugu (తెలుగు) if you have information. If you don't have information, you can say so in Telugu.",
            "tamil": "\n\nNote: Please respond in Tamil (தமிழ்) if you have information. If you don't have information, you can say so in Tamil.",
            "kannada": "\n\nNote: Please respond in Kannada (ಕನ್ನಡ) if you have information. If you don't have information, you can say so in Kannada.",
            "malayalam": "\n\nNote: Please respond in Malayalam (മലയാളം) if you have information. If you don't have information, you can say so in Malayalam.",
            "hindi": "\n\nNote: Please respond in Hindi (हिंदी) if you have information. If you don't have information, you can say so in Hindi.",
            "marathi": "\n\nNote: Please respond in Marathi (मराठी) if you have information. If you don't have information, you can say so in Marathi.",
            "bengali": "\n\nNote: Please respond in Bengali (বাংলা) if you have information. If you don't have information, you can say so in Bengali.",
            "gujarati": "\n\nNote: Please respond in Gujarati (ગુજરાતી) if you have information. If you don't have information, you can say so in Gujarati.",
            "punjabi": "\n\nNote: Please respond in Punjabi (ਪੰਜਾਬੀ) if you have information. If you don't have information, you can say so in Punjabi.",
            "odia": "\n\nNote: Please respond in Odia (ଓଡ଼ିଆ) if you have information. If you don't have information, you can say so in Odia.",
        }
    else:
        language_instructions = {
            "telugu": "\n\nIMPORTANT: You MUST respond ONLY in Telugu (తెలుగు) language. Do not use English or any other language in your response.",
            "tamil": "\n\nIMPORTANT: You MUST respond ONLY in Tamil (தமிழ்) language. Do not use English or any other language in your response.",
            "kannada": "\n\nIMPORTANT: You MUST respond ONLY in Kannada (ಕನ್ನಡ) language. Do not use English or any other language in your response.",
            "malayalam": "\n\nIMPORTANT: You MUST respond ONLY in Malayalam (മലയാളം) language. Do not use English or any other language in your response.",
            "hindi": "\n\nIMPORTANT: You MUST respond ONLY in Hindi (हिंदी) language. Do not use English or any other language in your response.",
            "marathi": "\n\nIMPORTANT: You MUST respond ONLY in Marathi (मराठी) language. Do not use English or any other language in your response.",
            "bengali": "\n\nIMPORTANT: You MUST respond ONLY in Bengali (বাংলা) language. Do not use English or any other language in your response.",
            "gujarati": "\n\nIMPORTANT: You MUST respond ONLY in Gujarati (ગુજરાતી) language. Do not use English or any other language in your response.",
            "punjabi": "\n\nIMPORTANT: You MUST respond ONLY in Punjabi (ਪੰਜਾਬੀ) language. Do not use English or any other language in your response.",
            "odia": "\n\nIMPORTANT: You MUST respond ONLY in Odia (ଓଡ଼ିଆ) language. Do not use English or any other language in your response.",
            "english": ""  # No need for instruction in English
        }
    
    language_instruction = language_instructions.get(language, "")
    enhanced_query = query + language_instruction
    
    payload = {
        "query": enhanced_query,
        "mode": mode,
        "conversation_history": history,
        "response_type": "Multiple Paragraphs"
    }
    res = requests.post(LIGHTRAG_URL, json=payload, timeout=60)
    return res.json().get("response", "")

