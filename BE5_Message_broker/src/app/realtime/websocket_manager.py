import asyncio
import logging
from typing import Any

from fastapi import WebSocket


logger = logging.getLogger("websocket_manager")


class WebSocketManager:
    """Ulangan WebSocket klientlarini boshqaradi."""

    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    @property
    def connection_count(self) -> int:
        return len(self._connections)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()

        async with self._lock:
            self._connections.add(websocket)

        logger.info(
            "WebSocket klient ulandi: active_connections=%s",
            self.connection_count,
        )

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections.discard(websocket)

        logger.info(
            "WebSocket klient uzildi: active_connections=%s",
            self.connection_count,
        )

    async def broadcast(
        self,
        payload: dict[str, Any],
    ) -> None:
        """
        Payload'ni barcha ulangan WebSocket klientlariga yuboradi.
        Ishlamaydigan ulanishlarni avtomatik tozalaydi.
        """

        async with self._lock:
            connections = list(self._connections)

        if not connections:
            logger.debug(
                "WebSocket broadcast o'tkazilmadi: klient mavjud emas"
            )
            return

        disconnected: list[WebSocket] = []

        for websocket in connections:
            try:
                await websocket.send_json(payload)
            except Exception:
                logger.exception(
                    "WebSocket klientga xabar yuborilmadi"
                )
                disconnected.append(websocket)

        if disconnected:
            async with self._lock:
                for websocket in disconnected:
                    self._connections.discard(websocket)

        logger.info(
            "WebSocket broadcast yakunlandi: "
            "sent=%s disconnected=%s",
            len(connections) - len(disconnected),
            len(disconnected),
        )


websocket_manager = WebSocketManager()
