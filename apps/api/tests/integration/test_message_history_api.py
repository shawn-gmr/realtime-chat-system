from libraries.message_history.service import MessageHistoryService


async def test_opening_conversation_returns_recent_history(session, seeded_messages) -> None:
    service = MessageHistoryService()
    payload = await service.get_history(
        session=session,
        conversation_id=seeded_messages["conversation_id"],
    )

    assert payload["conversation_id"] == str(seeded_messages["conversation_id"])
    assert len(payload["messages"]) == 3
