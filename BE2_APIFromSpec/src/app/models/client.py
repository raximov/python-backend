import uuid
from datetime import date, datetime

from app import db


class Client(db.Model):
    """Client entity for the appliance store."""
    __tablename__ = "clients"

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    client_name = db.Column(db.String(100), nullable=False)
    client_surname = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    registration_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    address_id = db.Column(
        db.String(36), db.ForeignKey("addresses.id"), nullable=True
    )

    # Relationship
    address = db.relationship("Address", backref="clients", lazy="joined")

    def __repr__(self) -> str:
        return f"<Client {self.client_name} {self.client_surname}>"
