import uuid

from app.dto.supplier import SupplierCreateDTO, SupplierResponseDTO
from app.models.supplier import Supplier


class SupplierMapper:
    @staticmethod
    def to_model(
        dto: SupplierCreateDTO,
        address_id: uuid.UUID,
    ) -> Supplier:
        return Supplier(
            name=dto.name,
            phone_number=dto.phone_number,
            address_id=address_id,
        )

    @staticmethod
    def to_response(model: Supplier) -> SupplierResponseDTO:
        return SupplierResponseDTO.model_validate(model)