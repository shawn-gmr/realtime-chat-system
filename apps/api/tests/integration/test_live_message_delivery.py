import uuid

from libraries.message_delivery.replay import build_history_sync_payload
from libraries.message_delivery.service import MessageDeliveryService
from observability.chat_telemetry import get_chat_telemetry


async def test_live_send_and_replay(session, seeded_conversation) -> None:
    service = MessageDeliveryService(get_chat_telemetry())
    message = await service.send_message(
        session=session,
        conversation_id=seeded_conversation["conversation_id"],
        sender_id=seeded_conversation["sender_id"],
        client_message_id=uuid.uuid4(),
        body="hello",
    )
    replay = await build_history_sync_payload(
        session=session,
        telemetry=get_chat_telemetry(),
        conversation_id=seeded_conversation["conversation_id"],
        last_seen_message_id=None,
    )

    assert message["body"] == "hello"
    assert replay["replay_complete"] is True
    assert len(replay["messages"]) == 1
