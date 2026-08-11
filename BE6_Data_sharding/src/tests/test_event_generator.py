import random
import uuid
from decimal import Decimal
from types import SimpleNamespace

from event_worker.generator import generate_product_update


def test_generator_changes_price_and_stock():
    product = SimpleNamespace(
        id=uuid.uuid4(),
        price=Decimal("100.00"),
        available_stock=10,
    )

    event = generate_product_update(
        product,
        rng=random.Random(42),
    )

    assert event.product_id == product.id
    assert event.price != product.price
    assert event.available_stock != product.available_stock
    assert event.price >= 0
    assert event.available_stock >= 0


def test_generator_handles_zero_values():
    product = SimpleNamespace(
        id=uuid.uuid4(),
        price=Decimal("0.00"),
        available_stock=0,
    )

    event = generate_product_update(
        product,
        rng=random.Random(7),
    )

    assert event.price == Decimal("0.01")
    assert event.available_stock > 0


def test_generator_creates_valid_event_type():
    product = SimpleNamespace(
        id=uuid.uuid4(),
        price=Decimal("250.50"),
        available_stock=3,
    )

    event = generate_product_update(
        product,
        rng=random.Random(15),
    )

    assert event.event_type == "product.attributes.updated"
    assert event.event_id is not None
    assert event.occurred_at.tzinfo is not None
