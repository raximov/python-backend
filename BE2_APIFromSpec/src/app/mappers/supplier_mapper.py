from app.models.supplier import Supplier
from app.mappers.address_mapper import AddressMapper


class SupplierMapper:
    """Maps between Supplier model and DTO dictionaries."""

    @staticmethod
    def to_entity(data: dict) -> Supplier:
        """Convert DTO dict to Supplier entity."""
        return Supplier(
            name=data["name"],
            phone_number=data.get("phone_number"),
        )

    @staticmethod
    def to_dto(supplier: Supplier) -> dict:
        """Convert Supplier entity to DTO dict."""
        return {
            "id": supplier.id,
            "name": supplier.name,
            "phone_number": supplier.phone_number,
            "address": AddressMapper.to_dto(supplier.address),
        }
