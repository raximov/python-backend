import uuid

from sqlalchemy import LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from photo_service.db.base import Base


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    image: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
    )
