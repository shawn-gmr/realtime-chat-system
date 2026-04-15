import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.chat import Message
from db.repositories.chat_repository import ChatRepository


def serialize_message(message: Message) -> dict[str, str | int | None]:
    return {
        "id": str(message.id),
        "conversation_id": str(message.conversation_id),
        "sender_id": str(message.sender_id),
        "body": message.body,
        "sent_at": message.sent_at.isoformat() if message.sent_at else None,
        "sequence_number": message.sequence_number,
    }


class MessageHistoryService:
    async def get_history(
        self,
        session: AsyncSession,
        conversation_id: uuid.UUID,
        before_message_id: uuid.UUID | None = None,
        limit: int = 50,
    ) -> dict[str, object]:
        repo = ChatRepository(session)
        page = await repo.list_history(
            conversation_id=conversation_id,
            before_message_id=before_message_id,
            limit=limit,
        )
        return {
            "conversation_id": str(conversation_id),
            "messages": [serialize_message(message) for message in page.messages],
            "has_more": page.has_more,
            "next_before_message_id": (
                str(page.next_before_message_id) if page.next_before_message_id is not None else None
            ),
        }
