import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.security.authorization import authorize
from app.dto.address import AddressCreateDTO
from app.dto.supplier import SupplierCreateDTO, SupplierResponseDTO
from app.services.supplier_service import SupplierService

router = APIRouter(tags=["Suppliers"])


@router.post(
    "",
    response_model=SupplierResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Add a supplier",
)
@authorize
def create_supplier(
    dto: SupplierCreateDTO,
    db: Session = Depends(get_db),
):
    return SupplierService(db).create(dto)


@router.get(
    "",
    response_model=list[SupplierResponseDTO],
    summary="Get all suppliers",
)
@authorize
def get_suppliers(
    db: Session = Depends(get_db),
):
    return SupplierService(db).get_all()


@router.get(
    "/{supplier_id}",
    response_model=SupplierResponseDTO,
    summary="Get supplier by id",
)
@authorize
def get_supplier(
    supplier_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    return SupplierService(db).get_by_id(supplier_id)


@router.patch(
    "/{supplier_id}/address",
    response_model=SupplierResponseDTO,
    summary="Change supplier address",
)
@authorize
def update_supplier_address(
    supplier_id: uuid.UUID,
    dto: AddressCreateDTO,
    db: Session = Depends(get_db),
):
    return SupplierService(db).update_address(
        supplier_id=supplier_id,
        dto=dto,
    )


@router.delete(
    "/{supplier_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete supplier",
)
@authorize
def delete_supplier(
    supplier_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    SupplierService(db).delete(supplier_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)