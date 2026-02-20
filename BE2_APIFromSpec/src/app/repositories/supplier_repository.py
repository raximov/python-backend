from app import db
from app.models.supplier import Supplier


class SupplierRepository:
    """Data Access Object for Supplier entity."""

    @staticmethod
    def create(supplier: Supplier) -> Supplier:
        """Create a new supplier."""
        db.session.add(supplier)
        db.session.commit()
        return supplier

    @staticmethod
    def get_by_id(supplier_id: str) -> Supplier | None:
        """Get supplier by ID."""
        return db.session.get(Supplier, supplier_id)

    @staticmethod
    def get_all() -> list[Supplier]:
        """Get all suppliers."""
        return Supplier.query.all()

    @staticmethod
    def update(supplier: Supplier) -> Supplier:
        """Update an existing supplier."""
        db.session.commit()
        return supplier

    @staticmethod
    def delete(supplier: Supplier) -> None:
        """Delete a supplier."""
        db.session.delete(supplier)
        db.session.commit()
