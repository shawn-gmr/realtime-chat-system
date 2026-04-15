import uuid


def build_presence_updated_event(conversation_id: uuid.UUID, presence: dict[str, object]) -> dict[str, object]:
    return {
        "type": "presence_updated",
        "conversation_id": str(conversation_id),
        "user_id": presence["user_id"],
        "status": presence["status"],
        "last_activity_at": presence["last_activity_at"],
        "scope": "global",
    }
