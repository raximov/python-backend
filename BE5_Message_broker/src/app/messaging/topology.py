from dataclasses import dataclass

from aio_pika import ExchangeType
from aio_pika.abc import (
    AbstractChannel,
    AbstractExchange,
    AbstractQueue,
)

from app.core.config import settings


@dataclass(frozen=True)
class RabbitTopology:
    exchange: AbstractExchange
    queue: AbstractQueue


async def declare_product_update_topology(
    channel: AbstractChannel,
) -> RabbitTopology:
    """Product update eventlari uchun exchange va queue yaratadi."""

    await channel.set_qos(prefetch_count=10)

    exchange = await channel.declare_exchange(
        name=settings.rabbitmq_exchange,
        type=ExchangeType.TOPIC,
        durable=True,
    )

    queue = await channel.declare_queue(
        name=settings.rabbitmq_queue,
        durable=True,
    )

    await queue.bind(
        exchange=exchange,
        routing_key=settings.rabbitmq_routing_key,
    )

    return RabbitTopology(
        exchange=exchange,
        queue=queue,
    )
