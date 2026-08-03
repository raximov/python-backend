import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreateDTO(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(ge=0)
    available_stock: int = Field(ge=0)
    supplier_id: uuid.UUID


class ProductResponseDTO(BaseModel):
    id: uuid.UUID
    name: str
    category: str
    price: Decimal
    available_stock: int
    last_update_date: datetime
    supplier_id: uuid.UUID
    image_id: uuid.UUID | None

    model_config = ConfigDict(from_attributes=True)


class ProductStockDecreaseDTO(BaseModel):
    quantity: int = Field(gt=0)