from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UserEntity:
    id: UUID
    email: str
    first_name: str
    last_name: str
    phone_number: str | None
    password_hash: str | None
    google_sub: str | None
    created_at: datetime
    updated_at: datetime
