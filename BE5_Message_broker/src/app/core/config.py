from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str

    grpc_host: str = "127.0.0.1"
    grpc_port: int = 50051

    rabbitmq_url: str = (
        "amqp://shop_mq_user:shop_mq_password@127.0.0.1:5673/"
    )
    rabbitmq_exchange: str = "product.events"
    rabbitmq_queue: str = "gateway.product.updates"
    rabbitmq_routing_key: str = "product.attributes.updated"

    redis_url: str = "redis://127.0.0.1:6380/0"
    image_cache_ttl_seconds: int = 3600

    event_generator_interval_seconds: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def auth_grpc_target(self) -> str:
        return f"{self.grpc_host}:{self.grpc_port}"


settings = Settings()
