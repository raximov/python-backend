import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.dto.address import AddressCreateDTO
from app.dto.client import ClientCreateDTO
from app.mappers.address_mapper import AddressMapper
from app.mappers.client_mapper import ClientMapper
from app.models.client import Client
from app.repositories.address_repository import AddressRepository
from app.repositories.client_repository import ClientRepository


class ClientService:
    def __init__(self, db: Session):
        self.db = db
        self.client_repository = ClientRepository(db)
        self.address_repository = AddressRepository(db)

    def create(self, dto: ClientCreateDTO) -> Client:
        try:
            address = AddressMapper.to_model(dto.address)
            self.address_repository.create(address)

            client = ClientMapper.to_model(
                dto=dto,
                address_id=address.id,
            )

            self.client_repository.create(client)
            client_id = client.id

            self.db.commit()

            created_client = self.client_repository.get_by_id(client_id)

            if created_client is None:
                raise NotFoundError("Client not found after creation")

            return created_client

        except Exception:
            self.db.rollback()
            raise

    def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Client]:
        return self.client_repository.get_all(
            limit=limit,
            offset=offset,
        )

    def get_by_name_and_surname(
        self,
        name: str,
        surname: str,
    ) -> list[Client]:
        return self.client_repository.get_by_name_and_surname(
            name=name,
            surname=surname,
        )

    def update_address(
        self,
        client_id: uuid.UUID,
        dto: AddressCreateDTO,
    ) -> Client:
        client = self.client_repository.get_by_id(client_id)

        if client is None:
            raise NotFoundError("Client not found")

        try:
            client.address.country = dto.country
            client.address.city = dto.city
            client.address.street = dto.street

            self.db.flush()
            self.db.commit()

            updated_client = self.client_repository.get_by_id(client_id)

            if updated_client is None:
                raise NotFoundError("Client not found")

            return updated_client

        except Exception:
            self.db.rollback()
            raise

    def delete(self, client_id: uuid.UUID) -> None:
        client = self.client_repository.get_by_id(client_id)

        if client is None:
            raise NotFoundError("Client not found")

        try:
            self.client_repository.delete(client)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise