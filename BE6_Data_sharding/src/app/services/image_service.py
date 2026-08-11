import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.cache.image_cache import image_cache
from app.clients.photo_client import PhotoClient
from app.core.exceptions import BadRequestError, NotFoundError
from app.repositories.product_repository import ProductRepository


@dataclass(frozen=True)
class ImageResult:
    id: uuid.UUID


@dataclass(frozen=True)
class ImageReadResult:
    id: uuid.UUID
    image: bytes
    cache_status: str


class ImageService:
    def __init__(
        self,
        db: Session,
        photo_client: PhotoClient | None = None,
    ):
        self.db = db
        self.product_repository = ProductRepository(db)
        self.photo_client = photo_client or PhotoClient()

    def add_to_product(
        self,
        product_id: uuid.UUID,
        image_bytes: bytes,
    ) -> ImageResult:
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise NotFoundError("Product not found")

        if not image_bytes:
            raise BadRequestError("Image cannot be empty")

        if product.image_id is not None:
            raise BadRequestError(
                "Product already has an image"
            )

        photo = self.photo_client.create(image_bytes)

        try:
            product.image_id = photo.id
            self.db.commit()
            self.db.refresh(product)
        except Exception:
            self.db.rollback()

            try:
                self.photo_client.delete(photo.id)
            except Exception:
                pass

            raise

        image_cache.set(photo.id, image_bytes)

        return ImageResult(id=photo.id)

    def update(
        self,
        image_id: uuid.UUID,
        image_bytes: bytes,
    ) -> ImageResult:
        if not image_bytes:
            raise BadRequestError("Image cannot be empty")

        photo = self.photo_client.update(
            image_id,
            image_bytes,
        )

        image_cache.set(photo.id, image_bytes)

        return ImageResult(id=photo.id)

    def _get_cached_or_remote(
        self,
        image_id: uuid.UUID,
    ) -> ImageReadResult:
        cached = image_cache.get(image_id)

        if cached is not None:
            return ImageReadResult(
                id=image_id,
                image=cached,
                cache_status="HIT",
            )

        image = self.photo_client.get(image_id)

        image_cache.set(image_id, image)

        return ImageReadResult(
            id=image_id,
            image=image,
            cache_status="MISS",
        )

    def get_by_id(
        self,
        image_id: uuid.UUID,
    ) -> ImageReadResult:
        return self._get_cached_or_remote(image_id)

    def get_by_product_id(
        self,
        product_id: uuid.UUID,
    ) -> ImageReadResult:
        product = self.product_repository.get_by_id(product_id)

        if product is None:
            raise NotFoundError("Product not found")

        if product.image_id is None:
            raise NotFoundError("Product image not found")

        return self._get_cached_or_remote(
            product.image_id
        )

    def delete(
        self,
        image_id: uuid.UUID,
    ) -> None:
        product = self.product_repository.get_by_image_id(
            image_id
        )

        if product is not None:
            try:
                product.image_id = None
                self.db.commit()
            except Exception:
                self.db.rollback()
                raise

        self.photo_client.delete(image_id)
        image_cache.delete(image_id)
