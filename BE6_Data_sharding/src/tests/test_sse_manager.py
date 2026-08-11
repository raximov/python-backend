import pytest

from app.realtime.sse_manager import (
    SSEManager,
    format_sse_message,
)


@pytest.mark.asyncio
async def test_sse_manager_connect_and_broadcast():
    manager = SSEManager()
    queue = await manager.connect()

    payload = {
        "type": "product.updated",
        "data": {
            "id": "product-id",
            "price": "100.00",
            "available_stock": 5,
        },
    }

    await manager.broadcast(payload)

    received = queue.get_nowait()

    assert manager.connection_count == 1
    assert received == payload


@pytest.mark.asyncio
async def test_sse_manager_disconnect():
    manager = SSEManager()
    queue = await manager.connect()

    await manager.disconnect(queue)

    assert manager.connection_count == 0


def test_format_sse_message():
    payload = {
        "type": "connection.ready",
        "data": {
            "message": "connected",
        },
    }

    result = format_sse_message(payload)

    assert result.startswith("data: ")
    assert '"type":"connection.ready"' in result
    assert result.endswith("\n\n")
