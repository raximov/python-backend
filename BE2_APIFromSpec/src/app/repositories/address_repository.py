from app import db
from app.models.address import Address


class AddressRepository:
    """Data Access Object for Address entity."""

    @staticmethod
    def create(address: Address) -> Address:
        """Create a new address."""
        db.session.add(address)
        db.session.commit()
        return address

    @staticmethod
    def get_by_id(address_id: str) -> Address | None:
        """Get address by ID."""
        return db.session.get(Address, address_id)

    @staticmethod
    def update(address: Address) -> Address:
        """Update an existing address."""
        db.session.commit()
        return address

    @staticmethod
    def delete(address: Address) -> None:
        """Delete an address."""
        db.session.delete(address)
        db.session.commit()
