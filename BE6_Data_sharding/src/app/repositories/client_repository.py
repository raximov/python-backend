import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.client import Client


class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, client: Client) -> Client:
        self.db.add(client)
        self.db.flush()
        return client

    def get_by_id(self, client_id: uuid.UUID) -> Client | None:
        statement = (
            select(Client)
            .options(joinedload(Client.address))
            .where(Client.id == client_id)
        )

        return self.db.scalar(statement)

    def get_by_name_and_surname(
        self,
        name: str,
        surname: str,
    ) -> list[Client]:
        statement = (
            select(Client)
            .options(joinedload(Client.address))
            .where(
                Client.client_name == name,
                Client.client_surname == surname,
            )
        )

        return list(self.db.scalars(statement).all())

    def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Client]:
        statement = (
            select(Client)
            .options(joinedload(Client.address))
            .order_by(Client.registration_date)
        )

        if offset is not None:
            statement = statement.offset(offset)

        if limit is not None:
            statement = statement.limit(limit)

        return list(self.db.scalars(statement).all())

    def delete(self, client: Client) -> None:
        self.db.delete(client)
        self.db.flush()