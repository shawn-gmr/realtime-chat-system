from pathlib import Path


def test_asyncapi_contains_realtime_frames() -> None:
    contract = Path("specs/001-realtime-chat-system/contracts/chat-realtime.asyncapi.yaml").read_text()
    assert "send_message" in contract
    assert "message_created" in contract
    assert "message_failed" in contract
    assert "presence_updated" in contract
