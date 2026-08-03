import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductAttributesUpdatedEvent(BaseModel):
    """Product narxi va mavjud qoldig‘i o‘zgargani haqidagi event."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    event_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
    )

    event_type: Literal["product.attributes.updated"] = (
        "product.attributes.updated"
    )

    product_id: uuid.UUID

    price: Decimal = Field(
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    available_stock: int = Field(ge=0)

    occurred_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @field_validator("occurred_at")
    @classmethod
    def validate_occurred_at(
        cls,
        value: datetime,
    ) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(
                "occurred_at timezone bilan berilishi kerak"
            )

        return value.astimezone(timezone.utc)
