from libraries.user_presence.service import UserPresenceService
from observability.chat_telemetry import get_chat_telemetry


async def test_reconnect_restores_presence_state(session, seeded_conversation) -> None:
    service = UserPresenceService(get_chat_telemetry())
    await service.mark_online(session, seeded_conversation["sender_id"])
    roster = await service.restore_presence_state(
        session=session,
        conversation_id=seeded_conversation["conversation_id"],
    )

    assert roster[0]["status"] == "online"
