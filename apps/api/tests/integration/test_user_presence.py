from libraries.user_presence.service import UserPresenceService
from observability.chat_telemetry import get_chat_telemetry


async def test_presence_transitions_online_then_offline(session, seeded_conversation) -> None:
    service = UserPresenceService(get_chat_telemetry())
    online = await service.mark_online(session, seeded_conversation["sender_id"])
    offline = await service.mark_offline(session, seeded_conversation["sender_id"])

    assert online["status"] == "online"
    assert offline["status"] == "offline"
