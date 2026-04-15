import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.conversation_access import (
    AuthenticatedUser,
    get_authenticated_user,
    require_conversation_participant,
)
from db.session import get_session
from libraries.user_presence.service import UserPresenceService
from observability.chat_telemetry import get_chat_telemetry

router = APIRouter(prefix="/api/conversations", tags=["chat-presence"])


@router.get("/{conversation_id}/presence")
async def get_conversation_presence(
    conversation_id: uuid.UUID,
    user: AuthenticatedUser = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_session),
) -> dict[str, object]:
    await require_conversation_participant(conversation_id=conversation_id, user=user, session=session)
    service = UserPresenceService(get_chat_telemetry())
    return {
        "conversation_id": str(conversation_id),
        "participants": await service.get_roster(session=session, conversation_id=conversation_id),
    }
