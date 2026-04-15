import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.conversation_access import (
    AuthenticatedUser,
    get_authenticated_user,
    require_conversation_participant,
)
from db.session import get_session
from libraries.message_history.service import MessageHistoryService

router = APIRouter(prefix="/api/conversations", tags=["chat-history"])


@router.get("/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: uuid.UUID,
    before_message_id: uuid.UUID | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_authenticated_user),
    session: AsyncSession = Depends(get_session),
) -> dict[str, object]:
    await require_conversation_participant(conversation_id=conversation_id, user=user, session=session)
    service = MessageHistoryService()
    return await service.get_history(
        session=session,
        conversation_id=conversation_id,
        before_message_id=before_message_id,
        limit=limit,
    )
