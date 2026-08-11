from aio_pika import DeliveryMode, Message
from aio_pika.abc import (
    AbstractExchange,
    AbstractRobustChannel,
    AbstractRobustConnection,
)

from app.messaging.connection import create_rabbitmq_connection
from app.messaging.schemas import ProductAttributesUpdatedEvent
from app.messaging.topology import declare_product_update_topology
from event_worker.config import worker_settings


class ProductEventProducer:
    def __init__(self) -> None:
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractRobustChannel | None = None
        self.exchange: AbstractExchange | None = None

    async def connect(self) -> None:
        self.connection = await create_rabbitmq_connection()
        self.channel = await self.connection.channel()

        topology = await declare_product_update_topology(
            self.channel
        )

        self.exchange = topology.exchange

    async def publish(
        self,
        event: ProductAttributesUpdatedEvent,
    ) -> None:
        if self.exchange is None:
            raise RuntimeError(
                "RabbitMQ producer hali ulanmagan"
            )

        message = Message(
            body=event.model_dump_json().encode("utf-8"),
            content_type="application/json",
            delivery_mode=DeliveryMode.PERSISTENT,
            message_id=str(event.event_id),
            type=event.event_type,
            headers={
                "occurred_at": event.occurred_at.isoformat(),
            },
        )

        await self.exchange.publish(
            message=message,
            routing_key=worker_settings.rabbitmq_routing_key,
        )

    async def close(self) -> None:
        if self.connection is not None:
            await self.connection.close()
