import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.dto.address import AddressCreateDTO
from app.dto.supplier import SupplierCreateDTO
from app.mappers.address_mapper import AddressMapper
from app.mappers.supplier_mapper import SupplierMapper
from app.models.supplier import Supplier
from app.repositories.address_repository import AddressRepository
from app.repositories.supplier_repository import SupplierRepository


class SupplierService:
    def __init__(self, db: Session):
        self.db = db
        self.supplier_repository = SupplierRepository(db)
        self.address_repository = AddressRepository(db)

    def create(self, dto: SupplierCreateDTO) -> Supplier:
        try:
            address = AddressMapper.to_model(dto.address)
            self.address_repository.create(address)

            supplier = SupplierMapper.to_model(
                dto=dto,
                address_id=address.id,
            )

            self.supplier_repository.create(supplier)
            supplier_id = supplier.id

            self.db.commit()

            created_supplier = self.supplier_repository.get_by_id(
                supplier_id
            )

            if created_supplier is None:
                raise NotFoundError("Supplier not found after creation")

            return created_supplier

        except Exception:
            self.db.rollback()
            raise

    def get_all(self) -> list[Supplier]:
        return self.supplier_repository.get_all()

    def get_by_id(self, supplier_id: uuid.UUID) -> Supplier:
        supplier = self.supplier_repository.get_by_id(supplier_id)

        if supplier is None:
            raise NotFoundError("Supplier not found")

        return supplier

    def update_address(
        self,
        supplier_id: uuid.UUID,
        dto: AddressCreateDTO,
    ) -> Supplier:
        supplier = self.supplier_repository.get_by_id(supplier_id)

        if supplier is None:
            raise NotFoundError("Supplier not found")

        try:
            supplier.address.country = dto.country
            supplier.address.city = dto.city
            supplier.address.street = dto.street

            self.db.flush()
            self.db.commit()

            updated_supplier = self.supplier_repository.get_by_id(
                supplier_id
            )

            if updated_supplier is None:
                raise NotFoundError("Supplier not found")

            return updated_supplier

        except Exception:
            self.db.rollback()
            raise

    def delete(self, supplier_id: uuid.UUID) -> None:
        supplier = self.supplier_repository.get_by_id(supplier_id)

        if supplier is None:
            raise NotFoundError("Supplier not found")

        try:
            self.supplier_repository.delete(supplier)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise