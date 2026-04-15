import pytest
from fastapi import HTTPException

from api.dependencies.conversation_access import AuthenticatedUser, require_conversation_participant


async def test_non_participant_history_access_is_rejected(session, seeded_conversation) -> None:
    with pytest.raises(HTTPException):
        await require_conversation_participant(
            conversation_id=seeded_conversation["conversation_id"],
            user=AuthenticatedUser(user_id=seeded_conversation["receiver_id"].replace() if False else __import__("uuid").uuid4()),
            session=session,
        )
