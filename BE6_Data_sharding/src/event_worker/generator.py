import random
from decimal import Decimal, ROUND_HALF_UP

from app.messaging.schemas import ProductAttributesUpdatedEvent
from app.models.product import Product


PRICE_FACTORS = (
    Decimal("0.90"),
    Decimal("0.95"),
    Decimal("1.05"),
    Decimal("1.10"),
)

STOCK_DELTAS = (
    -5,
    -4,
    -3,
    -2,
    -1,
    1,
    2,
    3,
    4,
    5,
)

MONEY_STEP = Decimal("0.01")


def generate_product_update(
    product: Product,
    rng: random.Random | None = None,
) -> ProductAttributesUpdatedEvent:
    """Product uchun yangi price va available_stock yaratadi."""

    randomizer = rng or random.SystemRandom()

    current_price = Decimal(product.price)
    price_factor = randomizer.choice(PRICE_FACTORS)

    new_price = (current_price * price_factor).quantize(
        MONEY_STEP,
        rounding=ROUND_HALF_UP,
    )

    # Juda kichik yoki 0 narxda yaxlitlash eski narxni qaytarishi mumkin.
    if new_price == current_price:
        new_price = current_price + MONEY_STEP

    stock_candidates = sorted(
        {
            max(0, product.available_stock + delta)
            for delta in STOCK_DELTAS
            if max(0, product.available_stock + delta)
            != product.available_stock
        }
    )

    if stock_candidates:
        new_available_stock = randomizer.choice(stock_candidates)
    else:
        new_available_stock = product.available_stock + 1

    return ProductAttributesUpdatedEvent(
        product_id=product.id,
        price=new_price,
        available_stock=new_available_stock,
    )
