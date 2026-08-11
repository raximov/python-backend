from typing import Any

import pytest

from app.realtime.websocket_manager import WebSocketManager


class FakeWebSocket:
    def __init__(self, fail_on_send: bool = False) -> None:
        self.accepted = False
        self.fail_on_send = fail_on_send
        self.messages: list[dict[str, Any]] = []

    async def accept(self) -> None:
        self.accepted = True

    async def send_json(
        self,
        payload: dict[str, Any],
    ) -> None:
        if self.fail_on_send:
            raise RuntimeError("Connection closed")

        self.messages.append(payload)


@pytest.mark.asyncio
async def test_websocket_manager_connect_and_broadcast():
    manager = WebSocketManager()
    websocket = FakeWebSocket()

    await manager.connect(websocket)

    payload = {
        "type": "product.updated",
        "data": {
            "id": "product-id",
            "price": "100.00",
            "available_stock": 5,
        },
    }

    await manager.broadcast(payload)

    assert websocket.accepted is True
    assert manager.connection_count == 1
    assert websocket.messages == [payload]


@pytest.mark.asyncio
async def test_websocket_manager_disconnect():
    manager = WebSocketManager()
    websocket = FakeWebSocket()

    await manager.connect(websocket)
    await manager.disconnect(websocket)

    assert manager.connection_count == 0


@pytest.mark.asyncio
async def test_websocket_manager_removes_broken_connection():
    manager = WebSocketManager()
    websocket = FakeWebSocket(fail_on_send=True)

    await manager.connect(websocket)
    await manager.broadcast(
        {
            "type": "product.updated",
            "data": {},
        }
    )

    assert manager.connection_count == 0
