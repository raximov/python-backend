import os
import bcrypt
from jose import jwt
from datetime import datetime, timedelta

JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_key_123")
JWT_ALGORITHM = "HS256"

class AuthServiceLogic:
    @staticmethod
    def get_password_hash(password: str) -> str:
        # bcrypt handles the salt automatically
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        password_byte_enc = plain_password.encode('utf-8')
        hashed_password_byte_enc = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password_byte_enc)

    @staticmethod
    def create_jwt_token(email: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode = {"sub": email, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def validate_jwt_token(token: str) -> str:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            email: str = payload.get("sub")
            return email
        except Exception:
            return None
