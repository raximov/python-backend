import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestError, NotFoundError
from app.dto.product import ProductCreateDTO
from app.mappers.product_mapper import ProductMapper
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.repositories.supplier_repository import SupplierRepository


class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.product_repository = ProductRepository(db)
        self.supplier_repository = SupplierRepository(db)

    def create(self, dto: ProductCreateDTO) -> Product:
        supplier = self.supplier_repository.get_by_id(dto.supplier_id)

        if supplier is None:
            raise NotFoundError("Supplier not found")

        try:
            product = ProductMapper.to_model(dto)

            self.product_repository.create(product)
            product_id = product.id

            self.db.commit()

            created_product = self.product_repository.get_by_id(
                product_id
            )

            if created_product is None:
                raise NotFoundError(
                    "Product not found after creation"
                )

            return created_product

        except Exception:
            self.db.rollback()
            raise

    def get_by_id(self, product_id: uuid.UUID) -> Product:
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise NotFoundError("Product not found")

        return product

    def get_available(self) -> list[Product]:
        return self.product_repository.get_available()

    def decrease_stock(
        self,
        product_id: uuid.UUID,
        quantity: int,
    ) -> Product:
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise NotFoundError("Product not found")

        if quantity <= 0:
            raise BadRequestError(
                "Quantity must be greater than zero"
            )

        if quantity > product.available_stock:
            raise BadRequestError(
                "Not enough product in stock"
            )

        try:
            product.available_stock -= quantity

            self.db.flush()
            self.db.commit()
            self.db.refresh(product)

            return product

        except Exception:
            self.db.rollback()
            raise

    def update_attributes(
        self,
        product_id: uuid.UUID,
        price: Decimal,
        available_stock: int,
        occurred_at: datetime,
    ) -> Product:
        """
        RabbitMQ eventidan kelgan narx va qoldiqni yangilaydi.
        """

        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise NotFoundError("Product not found")

        try:
            product.price = price
            product.available_stock = available_stock
            product.last_update_date = occurred_at

            self.db.flush()
            self.db.commit()
            self.db.refresh(product)

            return product

        except Exception:
            self.db.rollback()
            raise

    def delete(self, product_id: uuid.UUID) -> None:
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise NotFoundError("Product not found")

        try:
            self.product_repository.delete(product)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
