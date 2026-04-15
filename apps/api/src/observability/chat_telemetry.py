import logging
from functools import lru_cache

from pythonjsonlogger.json import JsonFormatter


class ChatTelemetry:
    def __init__(self) -> None:
        self.logger = logging.getLogger("chat.telemetry")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(JsonFormatter())
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def record_message_latency(self, conversation_id: str, latency_ms: float) -> None:
        self.logger.info(
            "message_latency",
            extra={"conversation_id": conversation_id, "latency_ms": latency_ms},
        )

    def record_replay(self, conversation_id: str, replay_count: int) -> None:
        self.logger.info(
            "reconnect_replay",
            extra={"conversation_id": conversation_id, "replay_count": replay_count},
        )

    def record_retry(self, client_message_id: str, succeeded: bool) -> None:
        self.logger.info(
            "message_retry",
            extra={"client_message_id": client_message_id, "succeeded": succeeded},
        )

    def record_presence_transition(self, user_id: str, status: str) -> None:
        self.logger.info(
            "presence_transition",
            extra={"user_id": user_id, "status": status},
        )


@lru_cache(maxsize=1)
def get_chat_telemetry() -> ChatTelemetry:
    return ChatTelemetry()
