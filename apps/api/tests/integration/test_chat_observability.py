from observability.chat_telemetry import get_chat_telemetry


def test_chat_telemetry_logger_exists() -> None:
    telemetry = get_chat_telemetry()
    assert telemetry.logger.name == "chat.telemetry"
