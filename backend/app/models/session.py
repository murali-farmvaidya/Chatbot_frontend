from datetime import datetime

def session_doc(user_id, title):
    return {
        "user_id": user_id,
        "title": title,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "followup_count": 0
    }
