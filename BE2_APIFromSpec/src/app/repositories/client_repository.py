from app import db
from app.models.client import Client


class ClientRepository:
    """Data Access Object for Client entity."""

    @staticmethod
    def create(client: Client) -> Client:
        """Create a new client."""
        db.session.add(client)
        db.session.commit()
        return client

    @staticmethod
    def get_by_id(client_id: str) -> Client | None:
        """Get client by ID."""
        return db.session.get(Client, client_id)

    @staticmethod
    def get_by_name(client_name: str, client_surname: str) -> list[Client]:
        """Get clients by first and last name."""
        query = Client.query
        if client_name:
            query = query.filter(Client.client_name.ilike(f"%{client_name}%"))
        if client_surname:
            query = query.filter(Client.client_surname.ilike(f"%{client_surname}%"))
        return query.all()

    @staticmethod
    def get_all(limit: int = None, offset: int = None) -> list[Client]:
        """Get all clients with optional pagination."""
        query = Client.query
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def update(client: Client) -> Client:
        """Update an existing client."""
        db.session.commit()
        return client

    @staticmethod
    def delete(client: Client) -> None:
        """Delete a client."""
        db.session.delete(client)
        db.session.commit()
