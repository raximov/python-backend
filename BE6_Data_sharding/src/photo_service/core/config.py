from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_host: str = Field(
        default="0.0.0.0",
        validation_alias="PHOTO_SERVICE_HOST",
    )
    service_port: int = Field(
        default=8001,
        validation_alias="PHOTO_SERVICE_PORT",
    )

    shard_1_url: str = Field(validation_alias="PHOTO_DB_1_URL")
    shard_2_url: str = Field(validation_alias="PHOTO_DB_2_URL")
    shard_3_url: str = Field(validation_alias="PHOTO_DB_3_URL")
    shard_4_url: str = Field(validation_alias="PHOTO_DB_4_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
