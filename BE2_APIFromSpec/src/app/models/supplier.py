import uuid

from app import db


class Supplier(db.Model):
    """Supplier entity for the appliance store."""
    __tablename__ = "suppliers"

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String(150), nullable=False)
    address_id = db.Column(
        db.String(36), db.ForeignKey("addresses.id"), nullable=True
    )
    phone_number = db.Column(db.String(20), nullable=True)

    # Relationship
    address = db.relationship("Address", backref="suppliers", lazy="joined")

    def __repr__(self) -> str:
        return f"<Supplier {self.name}>"
