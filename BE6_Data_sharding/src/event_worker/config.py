from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkerSettings(BaseSettings):
    readonly_database_url: str

    rabbitmq_url: str
    rabbitmq_exchange: str = "product.events"
    rabbitmq_routing_key: str = "product.attributes.updated"

    event_generator_interval_seconds: float = Field(
        default=5,
        gt=0,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


worker_settings = WorkerSettings()
