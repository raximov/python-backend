from app.models.address import Address


class AddressMapper:
    """Maps between Address model and DTO dictionaries."""

    @staticmethod
    def to_entity(data: dict) -> Address:
        """Convert DTO dict to Address entity."""
        return Address(
            country=data["country"],
            city=data["city"],
            street=data["street"],
        )

    @staticmethod
    def to_dto(address: Address) -> dict:
        """Convert Address entity to DTO dict."""
        if address is None:
            return None
        return {
            "id": address.id,
            "country": address.country,
            "city": address.city,
            "street": address.street,
        }
