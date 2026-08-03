from concurrent import futures
from contextlib import contextmanager
from collections.abc import Iterator

import grpc

from auth_service.container import container
from auth_service.core.config import auth_settings
from auth_service.domain.exceptions import (
    InvalidCredentialsError,
    InvalidInputError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from auth_service.infrastructure.database.session import AuthSessionLocal
from proto import auth_pb2, auth_pb2_grpc


@contextmanager
def service_scope() -> Iterator:
    db = AuthSessionLocal()

    try:
        repository = container.user_repository(session=db)
        service = container.auth_service(repository=repository)
        yield service
    finally:
        db.close()


def abort_for_auth_error(
    context: grpc.ServicerContext,
    exc: Exception,
) -> None:
    if isinstance(exc, UserAlreadyExistsError):
        context.abort(grpc.StatusCode.ALREADY_EXISTS, str(exc))

    if isinstance(exc, InvalidCredentialsError):
        context.abort(grpc.StatusCode.UNAUTHENTICATED, str(exc))

    if isinstance(exc, InvalidTokenError):
        context.abort(grpc.StatusCode.UNAUTHENTICATED, str(exc))

    if isinstance(exc, UserNotFoundError):
        context.abort(grpc.StatusCode.NOT_FOUND, str(exc))

    if isinstance(exc, InvalidInputError):
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))

    context.abort(grpc.StatusCode.INTERNAL, "Internal authorization service error")


class AuthGrpcServicer(auth_pb2_grpc.AuthServiceServicer):
    def Register(self, request, context):
        try:
            with service_scope() as service:
                token = service.register(
                    email=request.email,
                    first_name=request.first_name,
                    last_name=request.last_name,
                    phone_number=request.phone_number,
                    password=request.password,
                )

            return auth_pb2.TokenResponse(
                access_token=token,
                token_type="bearer",
            )
        except Exception as exc:
            abort_for_auth_error(context, exc)

    def Login(self, request, context):
        try:
            with service_scope() as service:
                token = service.login(
                    email=request.email,
                    password=request.password,
                )

            return auth_pb2.TokenResponse(
                access_token=token,
                token_type="bearer",
            )
        except Exception as exc:
            abort_for_auth_error(context, exc)

    def ValidateToken(self, request, context):
        try:
            with service_scope() as service:
                claims = service.validate_token(request.token)

            return auth_pb2.ValidateTokenResponse(
                valid=True,
                user_id=str(claims.user_id),
                email=claims.email,
            )
        except Exception as exc:
            abort_for_auth_error(context, exc)

    def ChangePassword(self, request, context):
        try:
            with service_scope() as service:
                service.change_password(
                    email=request.email,
                    current_password=request.current_password,
                    new_password=request.new_password,
                )

            return auth_pb2.OperationResponse(
                success=True,
                message="Password changed successfully",
            )
        except Exception as exc:
            abort_for_auth_error(context, exc)

    def ResetPassword(self, request, context):
        try:
            with service_scope() as service:
                service.reset_password(email=request.email)

            return auth_pb2.OperationResponse(
                success=True,
                message="Password reset successfully",
            )
        except Exception as exc:
            abort_for_auth_error(context, exc)


def serve() -> None:
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    auth_pb2_grpc.add_AuthServiceServicer_to_server(
        AuthGrpcServicer(),
        server,
    )

    address = f"{auth_settings.grpc_host}:{auth_settings.grpc_port}"

    server.add_insecure_port(address)
    server.start()

    print(
        f"Authorization gRPC service started on {address}",
        flush=True,
    )

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(grace=5)


if __name__ == "__main__":
    serve()
