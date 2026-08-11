import secrets

from auth_service.domain.entities.token_claims import TokenClaims
from auth_service.domain.exceptions import (
    InvalidCredentialsError,
    InvalidInputError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from auth_service.domain.interfaces.password_hasher import PasswordHasher
from auth_service.domain.interfaces.token_service import TokenService
from auth_service.domain.interfaces.user_repository import UserRepository


class AuthApplicationService:
    def __init__(
        self,
        *,
        repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ) -> None:
        self._repository = repository
        self._password_hasher = password_hasher
        self._token_service = token_service

    def register(
        self,
        *,
        email: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str,
    ) -> str:
        email = email.strip().lower()
        first_name = first_name.strip()
        last_name = last_name.strip()
        phone_number = phone_number.strip()

        if not all(
            [email, first_name, last_name, phone_number, password]
        ):
            raise InvalidInputError(
                "All registration fields are required"
            )

        if self._repository.get_by_email(email) is not None:
            raise UserAlreadyExistsError(
                "Email already registered"
            )

        if (
            self._repository.get_by_phone_number(phone_number)
            is not None
        ):
            raise UserAlreadyExistsError(
                "Phone number already registered"
            )

        password_hash = self._password_hasher.hash(password)

        user = self._repository.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password_hash=password_hash,
            google_sub=None,
        )

        return self._token_service.create_access_token(user)

    def login(
        self,
        *,
        email: str,
        password: str,
    ) -> str:
        email = email.strip().lower()

        user = self._repository.get_by_email(email)

        if user is None:
            raise InvalidCredentialsError(
                "Invalid email or password"
            )

        if user.password_hash is None:
            raise InvalidCredentialsError(
                "Use Google to sign in"
            )

        if not self._password_hasher.verify(
            password,
            user.password_hash,
        ):
            raise InvalidCredentialsError(
                "Invalid email or password"
            )

        return self._token_service.create_access_token(user)

    def google_login(
        self,
        *,
        email: str,
        first_name: str,
        last_name: str,
        google_sub: str,
    ) -> str:
        email = email.strip().lower()
        first_name = first_name.strip()
        last_name = last_name.strip()
        google_sub = google_sub.strip()

        if not email or not google_sub:
            raise InvalidInputError(
                "Google email and subject are required"
            )

        user = self._repository.get_by_google_sub(
            google_sub
        )

        if user is None:
            user = self._repository.get_by_email(email)

            if user is not None:
                if (
                    user.google_sub is not None
                    and user.google_sub != google_sub
                ):
                    raise InvalidCredentialsError(
                        "Google account mismatch"
                    )

                self._repository.set_google_sub(
                    user_id=user.id,
                    google_sub=google_sub,
                )

                user = self._repository.get_by_id(
                    user.id
                )

            else:
                if not first_name:
                    first_name = email.split("@", 1)[0]

                user = self._repository.create(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=None,
                    password_hash=None,
                    google_sub=google_sub,
                )

        if user is None:
            raise InvalidCredentialsError(
                "Unable to authenticate Google user"
            )

        return self._token_service.create_access_token(user)

    def validate_token(
        self,
        token: str,
    ) -> TokenClaims:
        claims = self._token_service.validate_access_token(
            token
        )

        if claims is None:
            raise InvalidTokenError(
                "Invalid or expired token"
            )

        user = self._repository.get_by_id(
            claims.user_id
        )

        if user is None:
            raise InvalidTokenError(
                "User does not exist"
            )

        return claims

    def change_password(
        self,
        *,
        email: str,
        current_password: str,
        new_password: str,
    ) -> None:
        user = self._repository.get_by_email(
            email.strip().lower()
        )

        if user is None:
            raise InvalidCredentialsError(
                "Invalid credentials"
            )

        if user.password_hash is None:
            raise InvalidCredentialsError(
                "Password authentication is not configured"
            )

        if not self._password_hasher.verify(
            current_password,
            user.password_hash,
        ):
            raise InvalidCredentialsError(
                "Invalid credentials"
            )

        if not new_password:
            raise InvalidInputError(
                "New password is required"
            )

        new_hash = self._password_hasher.hash(
            new_password
        )

        self._repository.update_password(
            user_id=user.id,
            password_hash=new_hash,
        )

    def reset_password(
        self,
        *,
        email: str,
    ) -> None:
        user = self._repository.get_by_email(
            email.strip().lower()
        )

        if user is None:
            raise UserNotFoundError(
                "User not found"
            )

        temporary_password = secrets.token_urlsafe(12)

        password_hash = self._password_hasher.hash(
            temporary_password
        )

        self._repository.update_password(
            user_id=user.id,
            password_hash=password_hash,
        )

        print(
            "\n"
            "========== EMAIL STUB ==========\n"
            f"To: {user.email}\n"
            "Subject: Password recovery\n"
            f"Temporary password: {temporary_password}\n"
            "================================\n",
            flush=True,
        )
