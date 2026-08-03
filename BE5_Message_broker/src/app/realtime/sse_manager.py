import asyncio
import json
import logging
from typing import Any


logger = logging.getLogger("sse_manager")

SSEQueue = asyncio.Queue[dict[str, Any]]


def format_sse_message(payload: dict[str, Any]) -> str:
    """Python dictionary'ni SSE xabari formatiga o'tkazadi."""

    data = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        default=str,
    )

    return f"data: {data}\n\n"


class SSEManager:
    """Ulangan SSE klientlarini alohida queue orqali boshqaradi."""

    def __init__(self) -> None:
        self._clients: set[SSEQueue] = set()
        self._lock = asyncio.Lock()

    @property
    def connection_count(self) -> int:
        return len(self._clients)

    async def connect(self) -> SSEQueue:
        queue: SSEQueue = asyncio.Queue(maxsize=100)

        async with self._lock:
            self._clients.add(queue)

        logger.info(
            "SSE klient ulandi: active_connections=%s",
            self.connection_count,
        )

        return queue

    async def disconnect(self, queue: SSEQueue) -> None:
        async with self._lock:
            self._clients.discard(queue)

        logger.info(
            "SSE klient uzildi: active_connections=%s",
            self.connection_count,
        )

    async def broadcast(
        self,
        payload: dict[str, Any],
    ) -> None:
        async with self._lock:
            clients = list(self._clients)

        if not clients:
            logger.debug(
                "SSE broadcast o'tkazilmadi: klient mavjud emas"
            )
            return

        for queue in clients:
            # Klient juda sekin bo'lsa, eng eski eventni olib tashlaymiz.
            if queue.full():
                try:
                    queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass

            queue.put_nowait(payload)

        logger.info(
            "SSE broadcast yakunlandi: sent=%s",
            len(clients),
        )


sse_manager = SSEManager()
