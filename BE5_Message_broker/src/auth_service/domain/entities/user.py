from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UserEntity:
    id: UUID
    email: str
    first_name: str
    last_name: str
    phone_number: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
