import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.chat_repository import ChatRepository
from libraries.message_history.service import serialize_message
from observability.chat_telemetry import ChatTelemetry


async def build_history_sync_payload(
    session: AsyncSession,
    telemetry: ChatTelemetry,
    conversation_id: uuid.UUID,
    last_seen_message_id: uuid.UUID | None,
) -> dict[str, object]:
    repo = ChatRepository(session)
    messages = await repo.replay_after(
        conversation_id=conversation_id,
        last_seen_message_id=last_seen_message_id,
    )
    telemetry.record_replay(conversation_id=str(conversation_id), replay_count=len(messages))
    return {
        "type": "history_synced",
        "conversation_id": str(conversation_id),
        "messages": [serialize_message(message) for message in messages],
        "replay_complete": True,
    }
