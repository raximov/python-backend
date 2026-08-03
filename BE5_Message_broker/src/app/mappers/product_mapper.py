from app.dto.product import ProductCreateDTO, ProductResponseDTO
from app.models.product import Product


class ProductMapper:
    @staticmethod
    def to_model(dto: ProductCreateDTO) -> Product:
        return Product(
            name=dto.name,
            category=dto.category,
            price=dto.price,
            available_stock=dto.available_stock,
            supplier_id=dto.supplier_id,
        )

    @staticmethod
    def to_response(model: Product) -> ProductResponseDTO:
        return ProductResponseDTO.model_validate(model)