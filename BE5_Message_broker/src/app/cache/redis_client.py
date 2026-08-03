from redis import Redis

from app.core.config import settings


redis_client = Redis.from_url(
    settings.redis_url,
    decode_responses=False,
    socket_connect_timeout=2,
    socket_timeout=2,
    health_check_interval=30,
)


def close_redis_client() -> None:
    """Redis connection pool'ni xavfsiz yopadi."""

    redis_client.close()
