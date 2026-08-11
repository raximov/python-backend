from photo_service.core.config import settings
from photo_service.db.factory import create_shard_engine, create_shard_session_factory

engine = create_shard_engine(settings.shard_2_url)
SessionLocal = create_shard_session_factory(engine)
