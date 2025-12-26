# app/services/chat_logic.py

from bson import ObjectId
from app.db.mongo import messages
from app.models.message import message_doc
from app.services.lightrag_service import query_lightrag
from app.utils.cleaner import clean_response
from app.services.followup_service import needs_follow_up

from app.services.chat_rules import (
    is_dosage_question,
    is_factual_company_question,
    is_direct_knowledge_question
)


def get_history(session_id):
    cursor = messages.find(
        {"session_id": session_id}
    ).sort("created_at", 1)

    return [{"role": m["role"], "content": m["content"]} for m in cursor]


def handle_chat(session_id, user_message):

    # 1️⃣ Save user message
    messages.insert_one(
        message_doc(session_id, "user", user_message)
    )

    history = get_history(session_id)

    # 2️⃣ DOSAGE → answer directly
    if is_dosage_question(user_message):
        answer = clean_response(
            query_lightrag(user_message, history)
        )
        messages.insert_one(
            message_doc(session_id, "assistant", answer)
        )
        return answer

    # 3️⃣ FACTUAL / COMPANY → answer directly
    if is_factual_company_question(user_message):
        answer = clean_response(
            query_lightrag(user_message, history)
        )
        messages.insert_one(
            message_doc(session_id, "assistant", answer)
        )
        return answer

    # 4️⃣ DIRECT PRODUCT / KNOWLEDGE → answer directly
    if is_direct_knowledge_question(user_message):
        answer = clean_response(
            query_lightrag(user_message, history)
        )
        messages.insert_one(
            message_doc(session_id, "assistant", answer)
        )
        return answer

    # 5️⃣ EVERYTHING ELSE → ask LLM if follow-up needed
    if needs_follow_up(session_id):
        followup = query_lightrag(
            "Ask ONE clear follow-up question to get missing farmer-specific details.",
            history,
            mode="bypass"
        )
        followup = followup.strip()

        messages.insert_one(
            message_doc(session_id, "assistant", followup)
        )
        return followup

    # 6️⃣ FINAL ANSWER
    answer = clean_response(
        query_lightrag(user_message, history)
    )
    messages.insert_one(
        message_doc(session_id, "assistant", answer)
    )
    return answer
