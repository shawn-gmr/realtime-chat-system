import uuid
from dataclasses import dataclass

from fastapi import Header, HTTPException, WebSocket, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.chat_repository import ChatRepository
from db.session import get_session


@dataclass(slots=True)
class AuthenticatedUser:
    user_id: uuid.UUID


async def get_authenticated_user(x_user_id: str = Header(alias="X-User-Id")) -> AuthenticatedUser:
    try:
        return AuthenticatedUser(user_id=uuid.UUID(x_user_id))
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing_auth") from exc


async def require_conversation_participant(
    conversation_id: uuid.UUID,
    user: AuthenticatedUser,
    session: AsyncSession,
) -> AuthenticatedUser:
    repo = ChatRepository(session)
    is_participant = await repo.user_is_participant(conversation_id=conversation_id, user_id=user.user_id)
    if not is_participant:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not_participant")
    return user


async def require_websocket_participant(
    websocket: WebSocket, conversation_id: uuid.UUID, session: AsyncSession
) -> uuid.UUID:
    user_id_header = websocket.headers.get("x-user-id")
    try:
        user_id = uuid.UUID(user_id_header or "")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing_auth") from exc
    repo = ChatRepository(session)
    is_participant = await repo.user_is_participant(conversation_id=conversation_id, user_id=user_id)
    if not is_participant:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not_participant")
    return user_id
