import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.security.authorization import authorize
from app.dto.product import (
    ProductCreateDTO,
    ProductResponseDTO,
    ProductStockDecreaseDTO,
)
from app.services.product_service import ProductService

router = APIRouter(tags=["Products"])


@router.post(
    "",
    response_model=ProductResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Add a product",
)
@authorize
def create_product(
    dto: ProductCreateDTO,
    db: Session = Depends(get_db),
):
    return ProductService(db).create(dto)


# MUHIM: /available /{product_id} dan oldin turadi.
@router.get(
    "/available",
    response_model=list[ProductResponseDTO],
    summary="Get all available products",
)
@authorize
def get_available_products(
    db: Session = Depends(get_db),
):
    return ProductService(db).get_available()


@router.get(
    "/{product_id}",
    response_model=ProductResponseDTO,
    summary="Get product by id",
)
@authorize
def get_product(
    product_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    return ProductService(db).get_by_id(product_id)


@router.patch(
    "/{product_id}/stock",
    response_model=ProductResponseDTO,
    summary="Decrease product stock",
)
@authorize
def decrease_product_stock(
    product_id: uuid.UUID,
    dto: ProductStockDecreaseDTO,
    db: Session = Depends(get_db),
):
    return ProductService(db).decrease_stock(
        product_id=product_id,
        quantity=dto.quantity,
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
)
@authorize
def delete_product(
    product_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    ProductService(db).delete(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)