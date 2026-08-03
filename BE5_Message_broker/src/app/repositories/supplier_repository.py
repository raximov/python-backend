import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.supplier import Supplier


class SupplierRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, supplier: Supplier) -> Supplier:
        self.db.add(supplier)
        self.db.flush()
        return supplier

    def get_by_id(self, supplier_id: uuid.UUID) -> Supplier | None:
        statement = (
            select(Supplier)
            .options(joinedload(Supplier.address))
            .where(Supplier.id == supplier_id)
        )

        return self.db.scalar(statement)

    def get_all(self) -> list[Supplier]:
        statement = (
            select(Supplier)
            .options(joinedload(Supplier.address))
            .order_by(Supplier.name)
        )

        return list(self.db.scalars(statement).all())

    def delete(self, supplier: Supplier) -> None:
        self.db.delete(supplier)
        self.db.flush()