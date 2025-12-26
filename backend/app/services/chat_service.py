from bson import ObjectId
from datetime import datetime
from app.db.mongo import messages, sessions
from app.models.message import message_doc
from app.services.lightrag_service import query_lightrag
from app.utils.cleaner import clean_response
from app.services.chat_logic import is_dosage_question, is_factual_company_question
from app.services.followup_service import (
    needs_follow_up,
    generate_followup,
    can_finalize
)

def generate_title(text: str) -> str:
    words = text.strip().split()
    return " ".join(words[:6]).capitalize()

def get_history(session_id):
    cursor = messages.find({"session_id": session_id}).sort("created_at", 1)
    return [{"role": m["role"], "content": m["content"]} for m in cursor]

def handle_chat(session_id, user_message):
    print("🔥 NEW HANDLE_CHAT EXECUTED")
    
    # Save user message
    messages.insert_one(message_doc(session_id, "user", user_message))

    # Update session timestamp
    sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"updated_at": datetime.utcnow()}}
    )

    # 🔥 COUNT messages AFTER insert
    msg_count = messages.count_documents({"session_id": session_id})

    # 🔥 FIRST USER MESSAGE = SET TITLE
    if msg_count == 1:
        title = generate_title(user_message)
        sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"title": title}}
        )

    session = sessions.find_one({"_id": ObjectId(session_id)})

    # 🚫 Dosage → direct answer always
    if is_dosage_question(user_message):
        print("✅ DOSAGE BRANCH RETURNING LIGHTRAG ANSWER")
        history = get_history(session_id)[:-1]
        answer = clean_response(query_lightrag(user_message, history))
        messages.insert_one(message_doc(session_id, "assistant", answer))
        return answer

    # � FACTUAL / COMPANY QUESTIONS → NEVER FOLLOW-UP
    if is_factual_company_question(user_message):
        history = get_history(session_id)[:-1]
        answer = clean_response(query_lightrag(user_message, history))
        messages.insert_one(message_doc(session_id, "assistant", answer))
        return answer

    # 🔁 FOLLOW-UP LOGIC
    if session.get("awaiting_followup") or needs_follow_up(session_id):

        if not can_finalize(session):
            followup_q = generate_followup(session_id)
            messages.insert_one(message_doc(session_id, "assistant", followup_q))
            return followup_q

        # Enough followups → finalize
        sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"awaiting_followup": False}}
        )

    # ✅ FINAL ANSWER
    history = get_history(session_id)[:-1]
    answer = clean_response(query_lightrag(user_message, history))
    messages.insert_one(message_doc(session_id, "assistant", answer))
    return answer
