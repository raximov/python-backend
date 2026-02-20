from app.dto.address_dto import AddressCreateDTO, AddressResponseDTO
from app.dto.client_dto import ClientCreateDTO, ClientResponseDTO, ClientUpdateAddressDTO
from app.dto.supplier_dto import SupplierCreateDTO, SupplierResponseDTO, SupplierUpdateAddressDTO
from app.dto.product_dto import ProductCreateDTO, ProductResponseDTO, ProductDecreaseStockDTO
from app.dto.image_dto import ImageResponseDTO

__all__ = [
    "AddressCreateDTO", "AddressResponseDTO",
    "ClientCreateDTO", "ClientResponseDTO", "ClientUpdateAddressDTO",
    "SupplierCreateDTO", "SupplierResponseDTO", "SupplierUpdateAddressDTO",
    "ProductCreateDTO", "ProductResponseDTO", "ProductDecreaseStockDTO",
    "ImageResponseDTO",
]
