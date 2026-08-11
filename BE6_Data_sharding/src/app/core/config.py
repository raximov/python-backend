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

    photo_service_url: str = "http://127.0.0.1:8001"
    photo_service_timeout_seconds: float = 5.0

    redis_url: str = "redis://127.0.0.1:6380/0"
    image_cache_ttl_seconds: int = 3600

    event_generator_interval_seconds: int = 5

    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = (
        "http://127.0.0.1:8000/auth/google/callback"
    )
    google_oauth_timeout_seconds: float = 10.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def auth_grpc_target(self) -> str:
        return f"{self.grpc_host}:{self.grpc_port}"


settings = Settings()
