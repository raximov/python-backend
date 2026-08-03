import logging
import uuid
from typing import Protocol

from redis.exceptions import RedisError

from app.cache.redis_client import redis_client
from app.core.config import settings


logger = logging.getLogger("image_cache")


class RedisClientProtocol(Protocol):
    def get(self, name: str) -> bytes | None:
        ...

    def set(
        self,
        name: str,
        value: bytes,
        *,
        ex: int | None = None,
    ) -> bool | None:
        ...

    def delete(self, *names: str) -> int:
        ...


class RedisImageCache:
    """Mahsulot rasmlarini Redis'da bytes ko‘rinishida saqlaydi."""

    KEY_PREFIX = "product:image"

    def __init__(
        self,
        client: RedisClientProtocol | None = None,
        ttl_seconds: int | None = None,
    ) -> None:
        self.client = client or redis_client
        self.ttl_seconds = (
            ttl_seconds
            if ttl_seconds is not None
            else settings.image_cache_ttl_seconds
        )

    def build_key(self, image_id: uuid.UUID) -> str:
        return f"{self.KEY_PREFIX}:{image_id}"

    def get(self, image_id: uuid.UUID) -> bytes | None:
        key = self.build_key(image_id)

        try:
            value = self.client.get(key)

        except RedisError:
            logger.exception(
                "Redis image cache GET ishlamadi: key=%s",
                key,
            )
            return None

        if value is None:
            logger.info(
                "Image cache MISS: image_id=%s",
                image_id,
            )
            return None

        logger.info(
            "Image cache HIT: image_id=%s",
            image_id,
        )

        return value

    def set(
        self,
        image_id: uuid.UUID,
        image_bytes: bytes,
    ) -> None:
        key = self.build_key(image_id)

        try:
            self.client.set(
                key,
                image_bytes,
                ex=self.ttl_seconds,
            )

            logger.info(
                "Image Redis'ga keshlangan: "
                "image_id=%s ttl=%s",
                image_id,
                self.ttl_seconds,
            )

        except RedisError:
            # Redis ishlamasa ham PostgreSQL requesti yiqilmaydi.
            logger.exception(
                "Redis image cache SET ishlamadi: key=%s",
                key,
            )

    def delete(self, image_id: uuid.UUID) -> None:
        key = self.build_key(image_id)

        try:
            self.client.delete(key)

            logger.info(
                "Image cache tozalandi: image_id=%s",
                image_id,
            )

        except RedisError:
            logger.exception(
                "Redis image cache DELETE ishlamadi: key=%s",
                key,
            )


image_cache = RedisImageCache()
