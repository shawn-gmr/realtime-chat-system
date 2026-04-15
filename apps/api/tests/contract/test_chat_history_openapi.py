from pathlib import Path


def test_openapi_contains_history_endpoint() -> None:
    contract = Path("specs/001-realtime-chat-system/contracts/chat-http.openapi.yaml").read_text()
    assert "/api/conversations/{conversation_id}/messages" in contract
    assert "before_message_id" in contract
    assert "next_before_message_id" in contract
