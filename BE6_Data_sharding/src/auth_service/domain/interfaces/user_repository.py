from abc import ABC, abstractmethod
from uuid import UUID

from auth_service.domain.entities.user import UserEntity


class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_phone_number(
        self,
        phone_number: str,
    ) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_google_sub(
        self,
        google_sub: str,
    ) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    def create(
        self,
        *,
        email: str,
        first_name: str,
        last_name: str,
        phone_number: str | None,
        password_hash: str | None,
        google_sub: str | None = None,
    ) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    def set_google_sub(
        self,
        *,
        user_id: UUID,
        google_sub: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_password(
        self,
        *,
        user_id: UUID,
        password_hash: str,
    ) -> None:
        raise NotImplementedError
