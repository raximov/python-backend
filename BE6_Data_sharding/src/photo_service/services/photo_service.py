import uuid

from photo_service.core.exceptions import EmptyPhotoError, PhotoNotFoundError
from photo_service.models.photo import Photo
from photo_service.repositories.photo_repository import PhotoRepository
from photo_service.sharding.router import get_session_factory


class PhotoService:
    def create(self, image_bytes: bytes) -> Photo:
        if not image_bytes:
            raise EmptyPhotoError("Photo cannot be empty")

        photo_id = uuid.uuid4()
        session_factory = get_session_factory(photo_id)

        with session_factory() as db:
            repository = PhotoRepository(db)

            try:
                photo = Photo(
                    id=photo_id,
                    image=image_bytes,
                )
                repository.create(photo)
                db.commit()
                db.refresh(photo)

                return Photo(
                    id=photo.id,
                    image=photo.image,
                )
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, photo_id: uuid.UUID) -> Photo:
        session_factory = get_session_factory(photo_id)

        with session_factory() as db:
            repository = PhotoRepository(db)
            photo = repository.get_by_id(photo_id)

            if photo is None:
                raise PhotoNotFoundError("Photo not found")

            return Photo(
                id=photo.id,
                image=photo.image,
            )

    def update(
        self,
        photo_id: uuid.UUID,
        image_bytes: bytes,
    ) -> Photo:
        if not image_bytes:
            raise EmptyPhotoError("Photo cannot be empty")

        session_factory = get_session_factory(photo_id)

        with session_factory() as db:
            repository = PhotoRepository(db)
            photo = repository.get_by_id(photo_id)

            if photo is None:
                raise PhotoNotFoundError("Photo not found")

            try:
                photo.image = image_bytes
                db.flush()
                db.commit()
                db.refresh(photo)

                return Photo(
                    id=photo.id,
                    image=photo.image,
                )
            except Exception:
                db.rollback()
                raise

    def delete(self, photo_id: uuid.UUID) -> None:
        session_factory = get_session_factory(photo_id)

        with session_factory() as db:
            repository = PhotoRepository(db)
            photo = repository.get_by_id(photo_id)

            if photo is None:
                raise PhotoNotFoundError("Photo not found")

            try:
                repository.delete(photo)
                db.commit()
            except Exception:
                db.rollback()
                raise
