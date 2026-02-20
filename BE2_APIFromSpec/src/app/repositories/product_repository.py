from datetime import datetime

from app import db
from app.models.product import Product


class ProductRepository:
    """Data Access Object for Product entity."""

    @staticmethod
    def create(product: Product) -> Product:
        """Create a new product."""
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def get_by_id(product_id: str) -> Product | None:
        """Get product by ID."""
        return db.session.get(Product, product_id)

    @staticmethod
    def get_all_available() -> list[Product]:
        """Get all products with available stock > 0."""
        return Product.query.filter(Product.available_stock > 0).all()

    @staticmethod
    def decrease_stock(product: Product, quantity: int) -> Product:
        """Decrease product stock and update last_update_date."""
        product.available_stock -= quantity
        product.last_update_date = datetime.utcnow()
        db.session.commit()
        return product

    @staticmethod
    def update(product: Product) -> Product:
        """Update an existing product."""
        db.session.commit()
        return product

    @staticmethod
    def delete(product: Product) -> None:
        """Delete a product."""
        db.session.delete(product)
        db.session.commit()
