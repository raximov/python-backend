from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth_service.domain.entities.user import UserEntity
from auth_service.domain.exceptions import UserAlreadyExistsError
from auth_service.domain.interfaces.user_repository import UserRepository
from auth_service.infrastructure.database.models.user import User


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    @staticmethod
    def _to_entity(model: User) -> UserEntity:
        return UserEntity(
            id=model.id,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            phone_number=model.phone_number,
            password_hash=model.password_hash,
            google_sub=model.google_sub,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def get_by_email(self, email: str) -> UserEntity | None:
        model = self._session.scalar(
            select(User).where(User.email == email)
        )
        return self._to_entity(model) if model else None

    def get_by_phone_number(
        self,
        phone_number: str,
    ) -> UserEntity | None:
        model = self._session.scalar(
            select(User).where(User.phone_number == phone_number)
        )
        return self._to_entity(model) if model else None

    def get_by_google_sub(
        self,
        google_sub: str,
    ) -> UserEntity | None:
        model = self._session.scalar(
            select(User).where(User.google_sub == google_sub)
        )
        return self._to_entity(model) if model else None

    def get_by_id(
        self,
        user_id: UUID,
    ) -> UserEntity | None:
        model = self._session.get(User, user_id)
        return self._to_entity(model) if model else None

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
        model = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password_hash=password_hash,
            google_sub=google_sub,
        )

        self._session.add(model)

        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise UserAlreadyExistsError(
                "User already exists"
            ) from exc

        self._session.refresh(model)
        return self._to_entity(model)

    def set_google_sub(
        self,
        *,
        user_id: UUID,
        google_sub: str,
    ) -> None:
        model = self._session.get(User, user_id)

        if model is None:
            return

        model.google_sub = google_sub

        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise UserAlreadyExistsError(
                "Google account already linked"
            ) from exc

    def update_password(
        self,
        *,
        user_id: UUID,
        password_hash: str,
    ) -> None:
        model = self._session.get(User, user_id)

        if model is None:
            return

        model.password_hash = password_hash
        self._session.commit()
