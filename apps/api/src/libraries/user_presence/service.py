import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.chat import UserPresence
from db.repositories.chat_repository import ChatRepository
from observability.chat_telemetry import ChatTelemetry


def serialize_presence(presence: UserPresence) -> dict[str, object]:
    return {
        "user_id": str(presence.user_id),
        "status": presence.status,
        "last_activity_at": presence.last_activity_at.isoformat() if presence.last_activity_at else None,
        "last_connected_at": (
            presence.last_connected_at.isoformat() if presence.last_connected_at else None
        ),
        "scope": "global",
    }


class UserPresenceService:
    def __init__(self, telemetry: ChatTelemetry):
        self.telemetry = telemetry

    async def mark_online(self, session: AsyncSession, user_id: uuid.UUID) -> dict[str, object]:
        repo = ChatRepository(session)
        presence = await repo.upsert_presence(user_id=user_id, status="online", active_connection_count=1)
        await session.commit()
        self.telemetry.record_presence_transition(user_id=str(user_id), status="online")
        return serialize_presence(presence)

    async def mark_offline(self, session: AsyncSession, user_id: uuid.UUID) -> dict[str, object]:
        repo = ChatRepository(session)
        presence = await repo.upsert_presence(user_id=user_id, status="offline", active_connection_count=0)
        await session.commit()
        self.telemetry.record_presence_transition(user_id=str(user_id), status="offline")
        return serialize_presence(presence)

    async def touch(self, session: AsyncSession, user_id: uuid.UUID) -> dict[str, object]:
        repo = ChatRepository(session)
        presence = await repo.upsert_presence(user_id=user_id, status="online", active_connection_count=1)
        await session.commit()
        return serialize_presence(presence)

    async def get_roster(
        self, session: AsyncSession, conversation_id: uuid.UUID
    ) -> list[dict[str, object]]:
        repo = ChatRepository(session)
        roster = await repo.list_presence_for_conversation(conversation_id=conversation_id)
        return [serialize_presence(presence) for presence in roster]

    async def restore_presence_state(
        self, session: AsyncSession, conversation_id: uuid.UUID
    ) -> list[dict[str, object]]:
        return await self.get_roster(session=session, conversation_id=conversation_id)
