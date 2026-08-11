import pytest

from photo_service.sharding.router import ShardNumber, get_shard_number


@pytest.mark.parametrize(
    ("photo_id", "expected"),
    [
        ("0fffffff-ffff-4fff-8fff-ffffffffffff", ShardNumber.SHARD_1),
        ("3fffffff-ffff-4fff-8fff-ffffffffffff", ShardNumber.SHARD_1),
        ("4fffffff-ffff-4fff-8fff-ffffffffffff", ShardNumber.SHARD_2),
        ("7fffffff-ffff-4fff-8fff-ffffffffffff", ShardNumber.SHARD_2),
        ("8fffffff-ffff-4fff-8fff-ffffffffffff", ShardNumber.SHARD_3),
        ("bfffffff-ffff-4fff-8fff-ffffffffffff", ShardNumber.SHARD_3),
        ("cfffffff-ffff-4fff-8fff-ffffffffffff", ShardNumber.SHARD_4),
        ("ffffffff-ffff-4fff-8fff-ffffffffffff", ShardNumber.SHARD_4),
    ],
)
def test_get_shard_number(photo_id, expected):
    assert get_shard_number(photo_id) == expected


def test_invalid_uuid():
    with pytest.raises(ValueError):
        get_shard_number("not-a-valid-uuid")
