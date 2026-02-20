import uuid

from app import db


class Address(db.Model):
    """Address entity - shared by clients and suppliers."""
    __tablename__ = "addresses"

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<Address {self.country}, {self.city}, {self.street}>"
