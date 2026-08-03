from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from auth_service.domain.entities.token_claims import TokenClaims
from auth_service.domain.entities.user import UserEntity
from auth_service.domain.interfaces.token_service import TokenService


class JWTTokenService(TokenService):
    def __init__(
        self,
        *,
        secret_key: str,
        algorithm: str,
        expire_minutes: int,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def create_access_token(self, user: UserEntity) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user.id),
            "email": user.email,
            "iat": now,
            "exp": now + timedelta(minutes=self._expire_minutes),
        }

        return jwt.encode(
            payload,
            self._secret_key,
            algorithm=self._algorithm,
        )

    def validate_access_token(self, token: str) -> TokenClaims | None:
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
            )

            user_id = UUID(payload["sub"])
            email = payload["email"]

            return TokenClaims(
                user_id=user_id,
                email=email,
            )
        except (jwt.PyJWTError, KeyError, ValueError):
            return None
