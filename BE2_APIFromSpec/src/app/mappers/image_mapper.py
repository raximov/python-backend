from app.models.image import Image


class ImageMapper:
    """Maps between Image model and DTO dictionaries."""

    @staticmethod
    def to_dto(image: Image, product_id: str = None) -> dict:
        """Convert Image entity to DTO dict."""
        return {
            "id": image.id,
            "product_id": product_id,
        }
