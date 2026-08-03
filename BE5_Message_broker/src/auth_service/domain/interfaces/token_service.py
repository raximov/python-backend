from abc import ABC, abstractmethod

from auth_service.domain.entities.token_claims import TokenClaims
from auth_service.domain.entities.user import UserEntity


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, user: UserEntity) -> str:
        raise NotImplementedError

    @abstractmethod
    def validate_access_token(self, token: str) -> TokenClaims | None:
        raise NotImplementedError
