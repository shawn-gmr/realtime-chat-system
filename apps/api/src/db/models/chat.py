import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.session import Base


class Conversation(Base):
    __tablename__ = "conversation"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_message_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    last_message_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    participants: Mapped[list["ConversationParticipant"]] = relationship(back_populates="conversation")
    messages: Mapped[list["Message"]] = relationship(back_populates="conversation")


class ConversationParticipant(Base):
    __tablename__ = "conversation_participant"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("conversation.id"), primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_read_message_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    last_read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    conversation: Mapped[Conversation] = relationship(back_populates="participants")


class Message(Base):
    __tablename__ = "message"
    __table_args__ = (
        UniqueConstraint(
            "conversation_id",
            "sender_id",
            "client_message_id",
            name="uq_message_sender_idempotency",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("conversation.id"), index=True
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), index=True)
    client_message_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True))
    body: Mapped[str] = mapped_column(Text())
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    sequence_number: Mapped[int] = mapped_column(Integer(), index=True)
    delivery_status: Mapped[str] = mapped_column(String(length=32), default="delivered")

    conversation: Mapped[Conversation] = relationship(back_populates="messages")


class UserPresence(Base):
    __tablename__ = "user_presence"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    status: Mapped[str] = mapped_column(String(length=16), default="offline")
    active_connection_count: Mapped[int] = mapped_column(Integer(), default=0)
    last_activity_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_connected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_disconnected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class WebSocketSession(Base):
    __tablename__ = "websocket_session"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("conversation.id"), index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), index=True)
    connected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_heartbeat_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    disconnected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    disconnect_reason: Mapped[str | None] = mapped_column(String(length=64), nullable=True)
