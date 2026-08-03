from dependency_injector import containers, providers

from auth_service.application.services.auth_service import (
    AuthApplicationService,
)
from auth_service.core.config import auth_settings
from auth_service.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from auth_service.infrastructure.security.argon2_password_hasher import (
    Argon2PasswordHasher,
)
from auth_service.infrastructure.security.jwt_token_service import (
    JWTTokenService,
)


class Container(containers.DeclarativeContainer):
    password_hasher = providers.Singleton(
        Argon2PasswordHasher,
    )

    token_service = providers.Singleton(
        JWTTokenService,
        secret_key=auth_settings.jwt_secret_key,
        algorithm=auth_settings.jwt_algorithm,
        expire_minutes=auth_settings.jwt_access_token_expire_minutes,
    )

    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
    )

    auth_service = providers.Factory(
        AuthApplicationService,
        password_hasher=password_hasher,
        token_service=token_service,
    )


container = Container()
