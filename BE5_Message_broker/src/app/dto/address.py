import uuid

from pydantic import BaseModel, ConfigDict, Field


class AddressCreateDTO(BaseModel):
    country: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    street: str = Field(min_length=1, max_length=255)


class AddressResponseDTO(BaseModel):
    id: uuid.UUID
    country: str
    city: str
    street: str

    model_config = ConfigDict(from_attributes=True)