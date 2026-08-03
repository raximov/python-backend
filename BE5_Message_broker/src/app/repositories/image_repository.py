import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.image import Image
from app.models.product import Product


class ImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, image: Image) -> Image:
        self.db.add(image)
        self.db.flush()
        return image

    def get_by_id(self, image_id: uuid.UUID) -> Image | None:
        return self.db.get(Image, image_id)

    def get_by_product_id(
        self,
        product_id: uuid.UUID,
    ) -> Image | None:
        statement = (
            select(Image)
            .join(Product, Product.image_id == Image.id)
            .where(Product.id == product_id)
        )

        return self.db.scalar(statement)

    def delete(self, image: Image) -> None:
        self.db.delete(image)
        self.db.flush()