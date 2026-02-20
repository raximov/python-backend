from app import db
from app.models.image import Image
from app.models.product import Product


class ImageRepository:
    """Data Access Object for Image entity."""

    @staticmethod
    def create(image: Image) -> Image:
        """Create a new image."""
        db.session.add(image)
        db.session.commit()
        return image

    @staticmethod
    def get_by_id(image_id: str) -> Image | None:
        """Get image by ID."""
        return db.session.get(Image, image_id)

    @staticmethod
    def get_by_product_id(product_id: str) -> Image | None:
        """Get image associated with a specific product."""
        product = db.session.get(Product, product_id)
        if product and product.image_id:
            return db.session.get(Image, product.image_id)
        return None

    @staticmethod
    def update(image: Image) -> Image:
        """Update an existing image."""
        db.session.commit()
        return image

    @staticmethod
    def delete(image: Image) -> None:
        """Delete an image."""
        db.session.delete(image)
        db.session.commit()
