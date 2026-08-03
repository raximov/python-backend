import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aio_pika.abc import (
    AbstractIncomingMessage,
    AbstractQueue,
    AbstractRobustConnection,
)
from pydantic import ValidationError
from aiormq.exceptions import ChannelInvalidStateError

from app.core.exceptions import NotFoundError
from app.db.session import SessionLocal
from app.dto.product import ProductResponseDTO
from app.messaging.connection import create_rabbitmq_connection
from app.messaging.schemas import ProductAttributesUpdatedEvent
from app.messaging.topology import declare_product_update_topology
from app.services.product_service import ProductService


logger = logging.getLogger("product_update_consumer")

ProductUpdatedCallback = Callable[
    [dict[str, Any]],
    Awaitable[None],
]


class ProductUpdateConsumer:
    """
    RabbitMQ'dan product update eventlarini qabul qiladi
    va PostgreSQL'dagi mahsulotni yangilaydi.
    """

    def __init__(
        self,
        on_product_updated: ProductUpdatedCallback | None = None,
    ) -> None:
        self.on_product_updated = on_product_updated
        self.connection: AbstractRobustConnection | None = None
        self.consumer_task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        if self.consumer_task is not None:
            return

        self.connection = await create_rabbitmq_connection()
        channel = await self.connection.channel()

        topology = await declare_product_update_topology(channel)

        self.consumer_task = asyncio.create_task(
            self._consume(topology.queue),
            name="product-update-consumer",
        )

        logger.info(
            "RabbitMQ consumer ishga tushdi: queue=%s",
            topology.queue.name,
        )

    async def _consume(
        self,
        queue: AbstractQueue,
    ) -> None:
        async with queue.iterator() as iterator:
            async for message in iterator:
                await self._process_message(message)

    async def _process_message(
        self,
        message: AbstractIncomingMessage,
    ) -> None:
        try:
            event = ProductAttributesUpdatedEvent.model_validate_json(
                message.body
            )

        except ValidationError:
            logger.exception(
                "Noto‘g‘ri event rad etildi: message_id=%s",
                message.message_id,
            )

            await message.reject(requeue=False)
            return

        try:
            product_payload = await asyncio.to_thread(
                self._update_product,
                event,
            )

            if self.on_product_updated is not None:
                await self.on_product_updated(product_payload)

        except NotFoundError:
            logger.exception(
                "Eventdagi mahsulot topilmadi: "
                "event_id=%s product_id=%s",
                event.event_id,
                event.product_id,
            )

            await message.reject(requeue=False)
            return

        except Exception:
            logger.exception(
                "Eventni qayta ishlashda xatolik: "
                "event_id=%s product_id=%s",
                event.event_id,
                event.product_id,
            )

            await message.nack(requeue=True)
            return

        await message.ack()

        logger.info(
            "Product yangilandi va event ACK qilindi: "
            "event_id=%s product_id=%s "
            "price=%s available_stock=%s",
            event.event_id,
            event.product_id,
            event.price,
            event.available_stock,
        )

    @staticmethod
    def _update_product(
        event: ProductAttributesUpdatedEvent,
    ) -> dict[str, Any]:
        with SessionLocal() as db:
            product = ProductService(db).update_attributes(
                product_id=event.product_id,
                price=event.price,
                available_stock=event.available_stock,
                occurred_at=event.occurred_at,
            )

            dto = ProductResponseDTO.model_validate(product)

            return dto.model_dump(mode="json")

    async def stop(self) -> None:
        """
        Consumer task va RabbitMQ connection'ni xavfsiz yopadi.

        Channel oldin yopilgan yoki task bekor qilingan holatlar
        application shutdown xatosiga aylantirilmaydi.
        """

        consumer_task = self.consumer_task
        self.consumer_task = None

        if consumer_task is not None:
            consumer_task.cancel()

            try:
                await consumer_task

            except asyncio.CancelledError:
                pass

            except ChannelInvalidStateError:
                logger.warning(
                    "RabbitMQ consumer yopilgan channel bilan yakunlandi"
                )

            except Exception:
                logger.exception(
                    "RabbitMQ consumer taskni yopishda xatolik"
                )

        connection = self.connection
        self.connection = None

        if connection is not None:
            try:
                await connection.close()

            except asyncio.CancelledError:
                pass

            except ChannelInvalidStateError:
                logger.warning(
                    "RabbitMQ connection oldin yopilgan"
                )

            except Exception:
                logger.exception(
                    "RabbitMQ connectionni yopishda xatolik"
                )

        logger.info("RabbitMQ consumer to‘xtatildi")
