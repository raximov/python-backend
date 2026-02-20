from app.models.product import Product


class ProductMapper:
    """Maps between Product model and DTO dictionaries."""

    @staticmethod
    def to_entity(data: dict) -> Product:
        """Convert DTO dict to Product entity."""
        return Product(
            name=data["name"],
            category=data["category"],
            price=data["price"],
            available_stock=data.get("available_stock", 0),
            supplier_id=data.get("supplier_id"),
        )

    @staticmethod
    def to_dto(product: Product) -> dict:
        """Convert Product entity to DTO dict."""
        return {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "available_stock": product.available_stock,
            "last_update_date": product.last_update_date.isoformat() if product.last_update_date else None,
            "supplier_id": product.supplier_id,
            "image_id": product.image_id,
        }
