import uuid
from datetime import datetime

from app import db


class Product(db.Model):
    """Product entity for the appliance store."""
    __tablename__ = "products"

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available_stock = db.Column(db.Integer, nullable=False, default=0)
    last_update_date = db.Column(
        db.DateTime, nullable=True, default=datetime.utcnow
    )
    supplier_id = db.Column(
        db.String(36), db.ForeignKey("suppliers.id"), nullable=True
    )
    image_id = db.Column(
        db.String(36), db.ForeignKey("images.id"), nullable=True
    )

    # Relationships
    supplier = db.relationship("Supplier", backref="products", lazy="joined")
    image = db.relationship("Image", backref="product", lazy="joined")

    def __repr__(self) -> str:
        return f"<Product {self.name}>"
