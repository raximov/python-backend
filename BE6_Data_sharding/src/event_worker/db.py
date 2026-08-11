from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from event_worker.config import worker_settings


worker_engine = create_engine(
    worker_settings.readonly_database_url,
    pool_pre_ping=True,
)

WorkerSessionLocal = sessionmaker(
    bind=worker_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
