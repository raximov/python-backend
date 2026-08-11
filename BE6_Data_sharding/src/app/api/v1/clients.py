import uuid

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.security.authorization import authorize
from app.dto.address import AddressCreateDTO
from app.dto.client import ClientCreateDTO, ClientResponseDTO
from app.services.client_service import ClientService

router = APIRouter(tags=["Clients"])


@router.post(
    "",
    response_model=ClientResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new client",
)
@authorize
def create_client(
    dto: ClientCreateDTO,
    db: Session = Depends(get_db),
):
    return ClientService(db).create(dto)


@router.get(
    "",
    response_model=list[ClientResponseDTO],
    summary="Get all clients",
)
@authorize
def get_clients(
    limit: int | None = Query(default=None, ge=1),
    offset: int | None = Query(default=None, ge=0),
    db: Session = Depends(get_db),
):
    return ClientService(db).get_all(
        limit=limit,
        offset=offset,
    )


@router.get(
    "/search",
    response_model=list[ClientResponseDTO],
    summary="Find clients by name and surname",
)
@authorize
def search_clients(
    name: str = Query(min_length=1),
    surname: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    return ClientService(db).get_by_name_and_surname(
        name=name,
        surname=surname,
    )


@router.patch(
    "/{client_id}/address",
    response_model=ClientResponseDTO,
    summary="Change client address",
)
@authorize
def update_client_address(
    client_id: uuid.UUID,
    dto: AddressCreateDTO,
    db: Session = Depends(get_db),
):
    return ClientService(db).update_address(
        client_id=client_id,
        dto=dto,
    )


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete client",
)
@authorize
def delete_client(
    client_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    ClientService(db).delete(client_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)