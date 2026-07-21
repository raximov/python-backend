import sys
import os

# Add current dir to path to find generated proto files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import grpc
from concurrent import futures
import auth_pb2
import auth_pb2_grpc
from database import SessionLocal, User
from services import AuthServiceLogic

class AuthHandler(auth_pb2_grpc.AuthServiceServicer):
    def Register(self, request, context):
        db = SessionLocal()
        try:
            # Check if user exists
            existing_user = db.query(User).filter(User.email == request.email).first()
            if existing_user:
                return auth_pb2.AuthResponse(token="", error="User already exists")

            hashed_password = AuthServiceLogic.get_password_hash(request.password)
            new_user = User(
                email=request.email,
                first_name=request.first_name,
                last_name=request.last_name,
                phone=request.phone,
                password_hash=hashed_password
            )
            db.add(new_user)
            db.commit()
            
            token = AuthServiceLogic.create_jwt_token(request.email)
            return auth_pb2.AuthResponse(token=token, error="")
        finally:
            db.close()

    def Authenticate(self, request, context):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == request.email).first()
            if not user or not AuthServiceLogic.verify_password(request.password, user.password_hash):
                return auth_pb2.AuthResponse(token="", error="Invalid email or password")
            
            token = AuthServiceLogic.create_jwt_token(user.email)
            return auth_pb2.AuthResponse(token=token, error="")
        finally:
            db.close()

    def ChangePassword(self, request, context):
        email = AuthServiceLogic.validate_jwt_token(request.token)
        if not email:
            return auth_pb2.StatusResponse(success=False, error="Invalid token")

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user or not AuthServiceLogic.verify_password(request.old_password, user.password_hash):
                return auth_pb2.StatusResponse(success=False, error="Invalid old password")
            
            user.password_hash = AuthServiceLogic.get_password_hash(request.new_password)
            db.commit()
            return auth_pb2.StatusResponse(success=True, error="")
        finally:
            db.close()

    def ResetPassword(self, request, context):
        # Stub for password reset (just prints to console as per methodology)
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == request.email).first()
            if user:
                # In a real app we'd generate a random password, save it, and email it.
                # Here we just print the stub
                print(f"[STUB] Отправка нового пароля на почту: {request.email} - Пожалуйста воспользуйтесь ссылкой для восстановления.")
            return auth_pb2.StatusResponse(success=True, error="")
        finally:
            db.close()

    def ValidateToken(self, request, context):
        email = AuthServiceLogic.validate_jwt_token(request.token)
        if email:
            return auth_pb2.ValidateTokenResponse(is_valid=True, user_email=email)
        return auth_pb2.ValidateTokenResponse(is_valid=False, user_email="")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthHandler(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC Auth Server starting on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
