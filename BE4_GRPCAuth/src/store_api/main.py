import sys
import os
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import grpc

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import auth_pb2
import auth_pb2_grpc
from middleware import GRPCAuthMiddleware

GRPC_HOST = os.getenv("AUTH_GRPC_HOST", "localhost")
GRPC_PORT = os.getenv("AUTH_GRPC_PORT", "50051")

app = FastAPI(title="Store API with gRPC Auth")

# Protect specific paths with our middleware
app.add_middleware(GRPCAuthMiddleware, protected_paths=["/protected_route"])

# ---- Dependency Injection (FastAPI style IoC) ----
def get_grpc_stub():
    channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")
    stub = auth_pb2_grpc.AuthServiceStub(channel)
    try:
        yield stub
    finally:
        channel.close()

# ---- Pydantic Schemas ----
class RegisterSchema(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str
    password: str

class AuthSchema(BaseModel):
    email: str
    password: str

class ResetPasswordSchema(BaseModel):
    email: str

# ---- Routes ----
@app.post("/register")
def register(data: RegisterSchema, stub: auth_pb2_grpc.AuthServiceStub = Depends(get_grpc_stub)):
    req = auth_pb2.RegisterRequest(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        phone=data.phone,
        password=data.password
    )
    try:
        res = stub.Register(req)
        if res.error:
            raise HTTPException(status_code=400, detail=res.error)
        return {"token": res.token}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())

@app.post("/auth")
def auth(data: AuthSchema, stub: auth_pb2_grpc.AuthServiceStub = Depends(get_grpc_stub)):
    req = auth_pb2.AuthRequest(email=data.email, password=data.password)
    try:
        res = stub.Authenticate(req)
        if res.error:
            raise HTTPException(status_code=401, detail=res.error)
        return {"token": res.token}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())

@app.post("/reset")
def reset_password(data: ResetPasswordSchema, stub: auth_pb2_grpc.AuthServiceStub = Depends(get_grpc_stub)):
    req = auth_pb2.ResetPasswordRequest(email=data.email)
    try:
        res = stub.ResetPassword(req)
        if not res.success:
            raise HTTPException(status_code=400, detail=res.error)
        return {"message": "Reset instructions printed to auth_service console"}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())

@app.get("/protected_route")
def protected_route():
    # If the request reaches here, it means the middleware successfully validated the token via gRPC
    return {"message": "You have accessed a protected route!", "info": "Your token is valid."}
