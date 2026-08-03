import uuid
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.messaging.schemas import ProductAttributesUpdatedEvent


def test_product_update_event_json_roundtrip():
    product_id = uuid.uuid4()

    event = ProductAttributesUpdatedEvent(
        product_id=product_id,
        price=Decimal("750000.00"),
        available_stock=14,
    )

    serialized = event.model_dump_json()

    restored = ProductAttributesUpdatedEvent.model_validate_json(
        serialized
    )

    assert restored.event_id == event.event_id
    assert restored.event_type == "product.attributes.updated"
    assert restored.product_id == product_id
    assert restored.price == Decimal("750000.00")
    assert restored.available_stock == 14
    assert restored.occurred_at.tzinfo is not None


def test_product_update_event_accepts_zero_price_and_stock():
    event = ProductAttributesUpdatedEvent(
        product_id=uuid.uuid4(),
        price=Decimal("0.00"),
        available_stock=0,
    )

    assert event.price == Decimal("0.00")
    assert event.available_stock == 0


def test_product_update_event_rejects_negative_stock():
    with pytest.raises(ValidationError):
        ProductAttributesUpdatedEvent(
            product_id=uuid.uuid4(),
            price=Decimal("750000.00"),
            available_stock=-1,
        )


def test_product_update_event_rejects_invalid_product_id():
    with pytest.raises(ValidationError):
        ProductAttributesUpdatedEvent(
            product_id="not-a-valid-uuid",
            price=Decimal("750000.00"),
            available_stock=14,
        )


def test_product_update_event_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        ProductAttributesUpdatedEvent(
            product_id=uuid.uuid4(),
            price=Decimal("750000.00"),
            available_stock=14,
            unknown_field="invalid",
        )
