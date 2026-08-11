from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


def create_shard_engine(database_url: str) -> Engine:
    return create_engine(
        database_url,
        pool_pre_ping=True,
    )


def create_shard_session_factory(engine: Engine) -> sessionmaker:
    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )
