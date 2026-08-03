import uuid

from app.cache.image_cache import RedisImageCache


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, bytes] = {}
        self.ttls: dict[str, int] = {}

    def get(self, name: str) -> bytes | None:
        return self.values.get(name)

    def set(
        self,
        name: str,
        value: bytes,
        *,
        ex: int | None = None,
    ) -> bool:
        self.values[name] = value

        if ex is not None:
            self.ttls[name] = ex

        return True

    def delete(self, *names: str) -> int:
        deleted = 0

        for name in names:
            if name in self.values:
                deleted += 1
                self.values.pop(name)
                self.ttls.pop(name, None)

        return deleted


def test_image_cache_set_and_get():
    client = FakeRedis()
    cache = RedisImageCache(
        client=client,
        ttl_seconds=3600,
    )

    image_id = uuid.uuid4()
    image_bytes = b"test-image-bytes"

    cache.set(image_id, image_bytes)

    assert cache.get(image_id) == image_bytes
    assert client.ttls[cache.build_key(image_id)] == 3600


def test_image_cache_returns_none_for_missing_key():
    cache = RedisImageCache(
        client=FakeRedis(),
        ttl_seconds=3600,
    )

    assert cache.get(uuid.uuid4()) is None


def test_image_cache_delete():
    client = FakeRedis()
    cache = RedisImageCache(
        client=client,
        ttl_seconds=3600,
    )

    image_id = uuid.uuid4()

    cache.set(image_id, b"image")
    cache.delete(image_id)

    assert cache.get(image_id) is None


def test_image_cache_key_format():
    cache = RedisImageCache(
        client=FakeRedis(),
        ttl_seconds=3600,
    )

    image_id = uuid.uuid4()

    assert cache.build_key(image_id) == (
        f"product:image:{image_id}"
    )
