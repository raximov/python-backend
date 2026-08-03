import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.cache.image_cache import image_cache
from app.core.exceptions import BadRequestError, NotFoundError
from app.models.image import Image
from app.repositories.image_repository import ImageRepository
from app.repositories.product_repository import ProductRepository


@dataclass(frozen=True)
class ImageReadResult:
    id: uuid.UUID
    image: bytes
    cache_status: str


class ImageService:
    def __init__(self, db: Session):
        self.db = db
        self.image_repository = ImageRepository(db)
        self.product_repository = ProductRepository(db)

    def add_to_product(
        self,
        product_id: uuid.UUID,
        image_bytes: bytes,
    ) -> Image:
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise NotFoundError("Product not found")

        if not image_bytes:
            raise BadRequestError("Image cannot be empty")

        if product.image_id is not None:
            raise BadRequestError(
                "Product already has an image"
            )

        try:
            image = Image(image=image_bytes)

            self.image_repository.create(image)
            product.image_id = image.id

            self.db.flush()
            self.db.commit()
            self.db.refresh(image)

        except Exception:
            self.db.rollback()
            raise

        # Faqat database commit muvaffaqiyatli bo‘lgandan keyin.
        image_cache.set(image.id, image.image)

        return image

    def update(
        self,
        image_id: uuid.UUID,
        image_bytes: bytes,
    ) -> Image:
        image = self.image_repository.get_by_id(image_id)

        if image is None:
            raise NotFoundError("Image not found")

        if not image_bytes:
            raise BadRequestError("Image cannot be empty")

        try:
            image.image = image_bytes

            self.db.flush()
            self.db.commit()
            self.db.refresh(image)

        except Exception:
            self.db.rollback()
            raise

        # Eski cache qiymati yangi rasm bilan almashtiriladi.
        image_cache.set(image.id, image.image)

        return image

    def _get_cached_or_database(
        self,
        image_id: uuid.UUID,
    ) -> ImageReadResult:
        cached_image = image_cache.get(image_id)

        if cached_image is not None:
            return ImageReadResult(
                id=image_id,
                image=cached_image,
                cache_status="HIT",
            )

        image = self.image_repository.get_by_id(image_id)

        if image is None:
            raise NotFoundError("Image not found")

        image_cache.set(image.id, image.image)

        return ImageReadResult(
            id=image.id,
            image=image.image,
            cache_status="MISS",
        )

    def get_by_id(
        self,
        image_id: uuid.UUID,
    ) -> ImageReadResult:
        return self._get_cached_or_database(image_id)

    def get_by_product_id(
        self,
        product_id: uuid.UUID,
    ) -> ImageReadResult:
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise NotFoundError("Product not found")

        if product.image_id is None:
            raise NotFoundError("Product image not found")

        return self._get_cached_or_database(
            product.image_id
        )

    def delete(self, image_id: uuid.UUID) -> None:
        image = self.image_repository.get_by_id(image_id)

        if image is None:
            raise NotFoundError("Image not found")

        try:
            self.image_repository.delete(image)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        # Database delete muvaffaqiyatli bo‘lgandan keyin cache tozalanadi.
        image_cache.delete(image_id)
