import uuid

from sqlalchemy.orm import Session

from photo_service.models.photo import Photo


class PhotoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, photo: Photo) -> Photo:
        self.db.add(photo)
        self.db.flush()
        return photo

    def get_by_id(self, photo_id: uuid.UUID) -> Photo | None:
        return self.db.get(Photo, photo_id)

    def delete(self, photo: Photo) -> None:
        self.db.delete(photo)
        self.db.flush()
