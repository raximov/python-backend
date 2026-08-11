import uuid

from app.dto.client import ClientCreateDTO, ClientResponseDTO
from app.models.client import Client


class ClientMapper:
    @staticmethod
    def to_model(
        dto: ClientCreateDTO,
        address_id: uuid.UUID,
    ) -> Client:
        return Client(
            client_name=dto.client_name,
            client_surname=dto.client_surname,
            birthday=dto.birthday,
            gender=dto.gender,
            address_id=address_id,
        )

    @staticmethod
    def to_response(model: Client) -> ClientResponseDTO:
        return ClientResponseDTO.model_validate(model)