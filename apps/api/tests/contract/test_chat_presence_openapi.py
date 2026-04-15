from pathlib import Path


def test_openapi_contains_presence_endpoint() -> None:
    contract = Path("specs/001-realtime-chat-system/contracts/chat-http.openapi.yaml").read_text()
    assert "/api/conversations/{conversation_id}/presence" in contract
    assert "scope" in contract
    assert "global" in contract
