from app.dto.address import AddressCreateDTO, AddressResponseDTO
from app.models.address import Address


class AddressMapper:
    @staticmethod
    def to_model(dto: AddressCreateDTO) -> Address:
        return Address(
            country=dto.country,
            city=dto.city,
            street=dto.street,
        )

    @staticmethod
    def to_response(model: Address) -> AddressResponseDTO:
        return AddressResponseDTO.model_validate(model)