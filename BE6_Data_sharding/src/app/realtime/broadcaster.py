import asyncio
from typing import Any

from app.realtime.sse_manager import sse_manager
from app.realtime.websocket_manager import websocket_manager


async def broadcast_product_update(
    product: dict[str, Any],
) -> None:
    payload = {
        "type": "product.updated",
        "data": product,
    }

    await asyncio.gather(
        websocket_manager.broadcast(payload),
        sse_manager.broadcast(payload),
    )
