import uuid

from app import db


class Image(db.Model):
    """Image entity - stores product images as binary data."""
    __tablename__ = "images"

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    image = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self) -> str:
        return f"<Image {self.id}>"
