import sys
import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import grpc

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import auth_pb2
import auth_pb2_grpc

GRPC_HOST = os.getenv("AUTH_GRPC_HOST", "localhost")
GRPC_PORT = os.getenv("AUTH_GRPC_PORT", "50051")

class GRPCAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, protected_paths: list[str]):
        super().__init__(app)
        self.protected_paths = protected_paths

    async def dispatch(self, request: Request, call_next):
        # Only check auth for paths that require it
        if not any(request.url.path.startswith(path) for path in self.protected_paths):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid Authorization header"})

        token = auth_header.split("Bearer ")[1]

        # Call gRPC service to validate token
        try:
            channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")
            stub = auth_pb2_grpc.AuthServiceStub(channel)
            validate_request = auth_pb2.ValidateTokenRequest(token=token)
            
            # Synchronous gRPC call (can be optimized with async grpc in production)
            response = stub.ValidateToken(validate_request)
            
            if not response.is_valid:
                return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})
                
            # Optionally attach user_email to request state for the controller to use
            request.state.user_email = response.user_email
            
        except grpc.RpcError as e:
            print(f"gRPC Error: {e.details()}")
            return JSONResponse(status_code=500, content={"detail": "Auth service unavailable"})

        return await call_next(request)
