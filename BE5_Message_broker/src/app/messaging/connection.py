import aio_pika
from aio_pika.abc import AbstractRobustConnection

from app.core.config import settings


async def create_rabbitmq_connection() -> AbstractRobustConnection:
    """RabbitMQ bilan avtomatik qayta ulanadigan connection yaratadi."""

    return await aio_pika.connect_robust(
        settings.rabbitmq_url,
    )
