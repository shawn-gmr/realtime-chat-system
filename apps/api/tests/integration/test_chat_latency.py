import uuid

from libraries.message_delivery.service import MessageDeliveryService
from observability.chat_telemetry import get_chat_telemetry


async def test_message_delivery_latency_path_executes(session, seeded_conversation) -> None:
    service = MessageDeliveryService(get_chat_telemetry())
    payload = await service.send_message(
        session=session,
        conversation_id=seeded_conversation["conversation_id"],
        sender_id=seeded_conversation["sender_id"],
        client_message_id=uuid.uuid4(),
        body="latency-check",
    )
    assert payload["body"] == "latency-check"
