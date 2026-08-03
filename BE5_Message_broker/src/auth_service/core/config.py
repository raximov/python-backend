from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    auth_database_url: str

    grpc_host: str = "127.0.0.1"
    grpc_port: int = 50051

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


auth_settings = AuthSettings()
