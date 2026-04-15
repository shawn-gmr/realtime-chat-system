import uuid
from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import Select, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.chat import ConversationParticipant, Message, UserPresence, WebSocketSession


@dataclass(slots=True)
class HistoryPage:
    messages: list[Message]
    has_more: bool
    next_before_message_id: uuid.UUID | None


class ChatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def user_is_participant(self, conversation_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        stmt = select(ConversationParticipant).where(
            ConversationParticipant.conversation_id == conversation_id,
            ConversationParticipant.user_id == user_id,
        )
        result = await self.session.scalar(stmt)
        return result is not None

    async def list_history(
        self,
        conversation_id: uuid.UUID,
        before_message_id: uuid.UUID | None = None,
        limit: int = 50,
    ) -> HistoryPage:
        query: Select[tuple[Message]] = select(Message).where(Message.conversation_id == conversation_id)
        if before_message_id is not None:
            anchor = await self.session.get(Message, before_message_id)
            if anchor is not None:
                query = query.where(Message.sequence_number < anchor.sequence_number)
        query = query.order_by(desc(Message.sequence_number)).limit(limit + 1)
        rows = list((await self.session.scalars(query)).all())
        has_more = len(rows) > limit
        page_rows = rows[:limit]
        next_before = page_rows[-1].id if has_more and page_rows else None
        return HistoryPage(messages=list(reversed(page_rows)), has_more=has_more, next_before_message_id=next_before)

    async def replay_after(
        self, conversation_id: uuid.UUID, last_seen_message_id: uuid.UUID | None
    ) -> list[Message]:
        query = select(Message).where(Message.conversation_id == conversation_id)
        if last_seen_message_id is not None:
            anchor = await self.session.get(Message, last_seen_message_id)
            if anchor is not None:
                query = query.where(Message.sequence_number > anchor.sequence_number)
        query = query.order_by(Message.sequence_number)
        return list((await self.session.scalars(query)).all())

    async def create_message(
        self,
        conversation_id: uuid.UUID,
        sender_id: uuid.UUID,
        client_message_id: uuid.UUID,
        body: str,
    ) -> Message:
        next_sequence = (
            await self.session.scalar(
                select(func.coalesce(func.max(Message.sequence_number), 0) + 1).where(
                    Message.conversation_id == conversation_id
                )
            )
        ) or 1
        message = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            client_message_id=client_message_id,
            body=body,
            sequence_number=next_sequence,
            delivery_status="delivered",
        )
        self.session.add(message)
        await self.session.flush()
        return message

    async def upsert_presence(
        self,
        user_id: uuid.UUID,
        status: str,
        active_connection_count: int,
    ) -> UserPresence:
        presence = await self.session.get(UserPresence, user_id)
        now = datetime.now(UTC)
        if presence is None:
            presence = UserPresence(
                user_id=user_id,
                status=status,
                active_connection_count=active_connection_count,
                last_activity_at=now,
                last_connected_at=now if status == "online" else None,
                last_disconnected_at=now if status == "offline" else None,
                updated_at=now,
            )
            self.session.add(presence)
        else:
            presence.status = status
            presence.active_connection_count = active_connection_count
            presence.last_activity_at = now
            presence.updated_at = now
            if status == "online":
                presence.last_connected_at = now
            if status == "offline":
                presence.last_disconnected_at = now
        await self.session.flush()
        return presence

    async def list_presence_for_conversation(self, conversation_id: uuid.UUID) -> list[UserPresence]:
        stmt = (
            select(UserPresence)
            .join(
                ConversationParticipant,
                ConversationParticipant.user_id == UserPresence.user_id,
            )
            .where(ConversationParticipant.conversation_id == conversation_id)
            .order_by(UserPresence.user_id)
        )
        return list((await self.session.scalars(stmt)).all())

    async def create_websocket_session(
        self, conversation_id: uuid.UUID, user_id: uuid.UUID
    ) -> WebSocketSession:
        session = WebSocketSession(conversation_id=conversation_id, user_id=user_id)
        self.session.add(session)
        await self.session.flush()
        return session
