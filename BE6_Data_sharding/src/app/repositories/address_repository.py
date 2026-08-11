import uuid

from sqlalchemy.orm import Session

from app.models.address import Address


class AddressRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, address: Address) -> Address:
        self.db.add(address)
        self.db.flush()
        return address

    def get_by_id(self, address_id: uuid.UUID) -> Address | None:
        return self.db.get(Address, address_id)

    def delete(self, address: Address) -> None:
        self.db.delete(address)
        self.db.flush()