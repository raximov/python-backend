from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from auth_service.core.config import auth_settings


auth_engine = create_engine(
    auth_settings.auth_database_url,
    pool_pre_ping=True,
)

AuthSessionLocal = sessionmaker(
    bind=auth_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_auth_db() -> Generator[Session, None, None]:
    db = AuthSessionLocal()

    try:
        yield db
    finally:
        db.close()
