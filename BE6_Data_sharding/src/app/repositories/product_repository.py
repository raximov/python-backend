import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.flush()
        return product

    def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        return self.db.get(Product, product_id)

    def get_available(self) -> list[Product]:
        statement = (
            select(Product)
            .where(Product.available_stock > 0)
            .order_by(Product.name)
        )

        return list(self.db.scalars(statement).all())

    def get_by_image_id(
        self,
        image_id: uuid.UUID,
    ) -> Product | None:
        statement = (
            select(Product)
            .where(Product.image_id == image_id)
        )
        return self.db.scalar(statement)

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.flush()