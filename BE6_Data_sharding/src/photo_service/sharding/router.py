from enum import IntEnum
from uuid import UUID


class ShardNumber(IntEnum):
    SHARD_1 = 1
    SHARD_2 = 2
    SHARD_3 = 3
    SHARD_4 = 4


def get_shard_number(photo_id: UUID | str) -> ShardNumber:
    """
    Select photo shard by the first hexadecimal character of UUID.

    0-3 -> shard 1
    4-7 -> shard 2
    8-b -> shard 3
    c-f -> shard 4
    """
    try:
        uuid_value = UUID(str(photo_id))
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError(f"Invalid photo UUID: {photo_id}") from exc

    first_char = str(uuid_value)[0].lower()

    if first_char in "0123":
        return ShardNumber.SHARD_1

    if first_char in "4567":
        return ShardNumber.SHARD_2

    if first_char in "89ab":
        return ShardNumber.SHARD_3

    if first_char in "cdef":
        return ShardNumber.SHARD_4

    raise ValueError(f"Unable to determine shard for UUID: {photo_id}")


def get_session_factory(photo_id: UUID | str):
    shard = get_shard_number(photo_id)

    if shard == ShardNumber.SHARD_1:
        from photo_service.db.shard_1 import SessionLocal
        return SessionLocal

    if shard == ShardNumber.SHARD_2:
        from photo_service.db.shard_2 import SessionLocal
        return SessionLocal

    if shard == ShardNumber.SHARD_3:
        from photo_service.db.shard_3 import SessionLocal
        return SessionLocal

    if shard == ShardNumber.SHARD_4:
        from photo_service.db.shard_4 import SessionLocal
        return SessionLocal

    raise RuntimeError(f"Unsupported shard: {shard}")
