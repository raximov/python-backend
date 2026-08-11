from photo_service.db.base import Base
from photo_service.db.shard_1 import engine as shard_1_engine
from photo_service.db.shard_2 import engine as shard_2_engine
from photo_service.db.shard_3 import engine as shard_3_engine
from photo_service.db.shard_4 import engine as shard_4_engine

# Model metadata ichiga ro'yxatdan o'tishi uchun.
from photo_service.models.photo import Photo  # noqa: F401


def init_shard_tables() -> None:
    engines = (
        shard_1_engine,
        shard_2_engine,
        shard_3_engine,
        shard_4_engine,
    )

    for engine in engines:
        Base.metadata.create_all(bind=engine)
