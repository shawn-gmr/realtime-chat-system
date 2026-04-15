import uuid

import pytest
from fastapi import HTTPException

from api.dependencies.conversation_access import require_websocket_participant


class DummyWebSocket:
    def __init__(self, user_id: str):
        self.headers = {"x-user-id": user_id}


async def test_non_participant_socket_access_is_rejected(session, seeded_conversation) -> None:
    websocket = DummyWebSocket(str(uuid.uuid4()))

    with pytest.raises(HTTPException):
        await require_websocket_participant(
            websocket=websocket,
            conversation_id=seeded_conversation["conversation_id"],
            session=session,
        )
