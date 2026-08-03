import asyncio
import logging
from collections.abc import AsyncGenerator

from fastapi import (
    APIRouter,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import StreamingResponse

from app.realtime.sse_manager import (
    format_sse_message,
    sse_manager,
)
from app.realtime.websocket_manager import websocket_manager


logger = logging.getLogger("realtime_api")

router = APIRouter(tags=["Realtime"])


@router.websocket("/ws/products")
async def product_updates_websocket(
    websocket: WebSocket,
) -> None:
    await websocket_manager.connect(websocket)

    try:
        await websocket.send_json(
            {
                "type": "connection.ready",
                "data": {
                    "message": (
                        "Product updates WebSocket connected"
                    ),
                },
            }
        )

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        logger.info(
            "WebSocket klient odatiy tarzda uzildi"
        )

    except Exception:
        logger.exception(
            "WebSocket ulanishida xatolik"
        )

    finally:
        await websocket_manager.disconnect(websocket)


@router.get(
    "/sse/products",
    summary="Stream product updates using SSE",
)
async def product_updates_sse(
    request: Request,
) -> StreamingResponse:
    queue = await sse_manager.connect()

    async def event_stream() -> AsyncGenerator[str, None]:
        try:
            yield format_sse_message(
                {
                    "type": "connection.ready",
                    "data": {
                        "message": (
                            "Product updates SSE connected"
                        ),
                    },
                }
            )

            while True:
                if await request.is_disconnected():
                    break

                try:
                    payload = await asyncio.wait_for(
                        queue.get(),
                        timeout=15,
                    )

                    yield format_sse_message(payload)

                except TimeoutError:
                    # Browser yoki proxy ulanishni yopib
                    # yubormasligi uchun keep-alive.
                    yield ": keep-alive\n\n"

        except asyncio.CancelledError:
            raise

        finally:
            await sse_manager.disconnect(queue)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
