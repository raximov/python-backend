import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.dto.address import AddressCreateDTO, AddressResponseDTO


class SupplierCreateDTO(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    phone_number: str = Field(min_length=1, max_length=32)
    address: AddressCreateDTO


class SupplierResponseDTO(BaseModel):
    id: uuid.UUID
    name: str
    phone_number: str
    address: AddressResponseDTO

    model_config = ConfigDict(from_attributes=True)