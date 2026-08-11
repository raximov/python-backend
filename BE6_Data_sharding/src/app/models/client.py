import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING
from app.models.address import Address
from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.address import Address


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    client_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    client_surname: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    birthday: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    registration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    address_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("addresses.id"),
        nullable=False,
        index=True,
    )

    address: Mapped["Address"] = relationship()