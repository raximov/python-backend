from app.models.client import Client
from app.mappers.address_mapper import AddressMapper


class ClientMapper:
    """Maps between Client model and DTO dictionaries."""

    @staticmethod
    def to_entity(data: dict) -> Client:
        """Convert DTO dict to Client entity."""
        return Client(
            client_name=data["client_name"],
            client_surname=data["client_surname"],
            birthday=data.get("birthday"),
            gender=data.get("gender"),
        )

    @staticmethod
    def to_dto(client: Client) -> dict:
        """Convert Client entity to DTO dict."""
        return {
            "id": client.id,
            "client_name": client.client_name,
            "client_surname": client.client_surname,
            "birthday": client.birthday.isoformat() if client.birthday else None,
            "gender": client.gender,
            "registration_date": client.registration_date.isoformat() if client.registration_date else None,
            "address": AddressMapper.to_dto(client.address),
        }
