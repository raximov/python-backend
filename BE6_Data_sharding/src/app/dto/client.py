import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.dto.address import AddressCreateDTO, AddressResponseDTO


class ClientCreateDTO(BaseModel):
    client_name: str = Field(min_length=1, max_length=100)
    client_surname: str = Field(min_length=1, max_length=100)
    birthday: date
    gender: str = Field(min_length=1, max_length=20)
    address: AddressCreateDTO


class ClientResponseDTO(BaseModel):
    id: uuid.UUID
    client_name: str
    client_surname: str
    birthday: date
    gender: str
    registration_date: datetime
    address: AddressResponseDTO

    model_config = ConfigDict(from_attributes=True)