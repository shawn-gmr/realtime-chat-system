import uuid
from time import perf_counter

from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.chat_repository import ChatRepository
from libraries.message_history.service import serialize_message
from observability.chat_telemetry import ChatTelemetry


class MessageDeliveryService:
    def __init__(self, telemetry: ChatTelemetry):
        self.telemetry = telemetry

    async def send_message(
        self,
        session: AsyncSession,
        conversation_id: uuid.UUID,
        sender_id: uuid.UUID,
        client_message_id: uuid.UUID,
        body: str,
    ) -> dict[str, object]:
        trimmed_body = body.strip()
        if not trimmed_body:
            raise ValueError("message_body_required")

        repo = ChatRepository(session)
        started_at = perf_counter()
        message = await repo.create_message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            client_message_id=client_message_id,
            body=trimmed_body,
        )
        await session.commit()
        self.telemetry.record_message_latency(
            conversation_id=str(conversation_id),
            latency_ms=(perf_counter() - started_at) * 1000,
        )
        return serialize_message(message)
