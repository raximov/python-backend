import grpc

from app.core.config import settings
from proto import auth_pb2, auth_pb2_grpc


class AuthGrpcClient:
    def __init__(self, target: str) -> None:
        self._channel = grpc.insecure_channel(target)
        self._stub = auth_pb2_grpc.AuthServiceStub(self._channel)

    def register(
        self,
        *,
        email: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        password: str,
    ):
        return self._stub.Register(
            auth_pb2.RegisterRequest(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                password=password,
            )
        )

    def login(
        self,
        *,
        email: str,
        password: str,
    ):
        return self._stub.Login(
            auth_pb2.LoginRequest(
                email=email,
                password=password,
            )
        )

    def reset_password(self, *, email: str):
        return self._stub.ResetPassword(
            auth_pb2.ResetPasswordRequest(
                email=email,
            )
        )

    def validate_token(self, token: str):
        return self._stub.ValidateToken(
            auth_pb2.ValidateTokenRequest(
                token=token,
            )
        )


auth_grpc_client = AuthGrpcClient(
    settings.auth_grpc_target,
)
