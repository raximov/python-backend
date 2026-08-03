from pathlib import Path


CLIENTS_DIR = (
    Path(__file__).resolve().parents[1] / "clients"
)


def test_websocket_client_exists_and_connects():
    path = CLIENTS_DIR / "websocket-client.html"

    assert path.is_file()

    content = path.read_text(encoding="utf-8")

    assert "new WebSocket" in content
    assert "/ws/products" in content
    assert "console.log" in content


def test_sse_client_exists_and_connects():
    path = CLIENTS_DIR / "sse-client.html"

    assert path.is_file()

    content = path.read_text(encoding="utf-8")

    assert "new EventSource" in content
    assert "/sse/products" in content
    assert "console.log" in content
