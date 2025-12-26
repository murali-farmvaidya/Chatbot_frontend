# app/services/chat_rules.py

def normalize(text: str) -> str:
    return text.lower().replace(" ", "").replace("-", "")


# ---------------- DOSAGE ----------------
def is_dosage_question(text: str) -> bool:
    keywords = [
        "dosage", "dose", "how much",
        "quantity", "per acre", "for acres",
        "application rate"
    ]
    t = text.lower()
    return any(k in t for k in keywords)


# ---------------- FACTUAL / COMPANY ----------------
def is_factual_company_question(text: str) -> bool:
    keywords = [
        "who is", "ceo", "founder", "director",
        "how many", "number of", "count",
        "patents", "years", "established",
        "headquarters"
    ]

    entities = [
        "biofactor",
        "farmvaidya",
        "aadhaar",
        "poshak",
        "invictus"
    ]

    t = normalize(text)

    return (
        any(k.replace(" ", "") in t for k in keywords)
        and any(e in t for e in entities)
    )


# ---------------- DIRECT PRODUCT / KNOWLEDGE ----------------
def is_direct_knowledge_question(text: str) -> bool:
    keywords = [
        "what is", "tell me", "explain",
        "usage", "how is it used",
        "benefits", "features"
    ]

    products = [
        "aadhaar gold",
        "poshak",
        "invictus",
        "zn-factor",
        "biofactor",
        "farmvaidya"
    ]

    t = text.lower()
    return any(k in t for k in keywords) and any(p in t for p in products)
