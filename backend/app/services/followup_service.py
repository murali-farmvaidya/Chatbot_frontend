from app.services.lightrag_service import query_lightrag
from app.db.mongo import sessions, messages
from bson import ObjectId

MAX_FOLLOWUPS = 2

def needs_follow_up(session_id: str) -> bool:
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in messages.find({"session_id": session_id}).sort("created_at", 1)
    ]

    payload = {
        "query": (
            "You are an agriculture assistant.\n\n"
            "Ask a follow-up question ONLY IF:\n"
            "- The answer depends on farmer-specific inputs "
            "(crop, growth stage, soil, symptoms, location).\n\n"
            "Reply ONLY with:\n"
            "ANSWER_DIRECTLY or ASK_FOLLOW_UP"
        ),
        "mode": "bypass",
        "conversation_history": history,
        "response_type": "Single Sentence"
    }

    res = query_lightrag(payload["query"], history, mode="bypass")
    return res.strip().upper() == "ASK_FOLLOW_UP"


def generate_followup(session_id: str) -> str:
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in messages.find({"session_id": session_id}).sort("created_at", 1)
    ]

    payload = {
        "query": "Ask ONE clear follow-up question to get missing farmer-specific details.",
        "mode": "bypass",
        "conversation_history": history,
        "response_type": "Single Sentence"
    }

    question = query_lightrag(payload["query"], history, mode="bypass")

    sessions.update_one(
        {"_id": ObjectId(session_id)},
        {
            "$inc": {"followup_count": 1},
            "$set": {"awaiting_followup": True}
        }
    )

    return question.strip()


def can_finalize(session):
    return session.get("followup_count", 0) >= MAX_FOLLOWUPS
