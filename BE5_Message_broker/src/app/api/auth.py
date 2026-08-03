import grpc
from fastapi import APIRouter, HTTPException, status

from app.dto.auth import (
    LoginDTO,
    OperationDTO,
    RegisterDTO,
    ResetPasswordDTO,
    TokenDTO,
)
from app.grpc.auth_client import auth_grpc_client


router = APIRouter(tags=["Authentication"])


def _handle_grpc_error(exc: grpc.RpcError) -> None:
    code = exc.code()
    detail = exc.details() or "Authorization service error"

    if code == grpc.StatusCode.ALREADY_EXISTS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )

    if code == grpc.StatusCode.UNAUTHENTICATED:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )

    if code == grpc.StatusCode.NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

    if code == grpc.StatusCode.INVALID_ARGUMENT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )

    if code == grpc.StatusCode.UNAVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authorization service is unavailable",
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Authorization service error",
    )


@router.post(
    "/register",
    response_model=TokenDTO,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: RegisterDTO) -> TokenDTO:
    try:
        response = auth_grpc_client.register(
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            phone_number=payload.phone_number,
            password=payload.password,
        )
    except grpc.RpcError as exc:
        _handle_grpc_error(exc)
        raise

    return TokenDTO(
        access_token=response.access_token,
        token_type=response.token_type,
    )


@router.post(
    "/auth",
    response_model=TokenDTO,
)
def authenticate(payload: LoginDTO) -> TokenDTO:
    try:
        response = auth_grpc_client.login(
            email=payload.email,
            password=payload.password,
        )
    except grpc.RpcError as exc:
        _handle_grpc_error(exc)
        raise

    return TokenDTO(
        access_token=response.access_token,
        token_type=response.token_type,
    )


@router.post(
    "/reset",
    response_model=OperationDTO,
)
def reset_password(payload: ResetPasswordDTO) -> OperationDTO:
    try:
        response = auth_grpc_client.reset_password(
            email=payload.email,
        )
    except grpc.RpcError as exc:
        _handle_grpc_error(exc)
        raise

    return OperationDTO(
        success=response.success,
        message=response.message,
    )
