from pydantic import BaseModel, Field


class RegisterDTO(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone_number: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=1)


class LoginDTO(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=1)


class ResetPasswordDTO(BaseModel):
    email: str = Field(min_length=3, max_length=320)


class TokenDTO(BaseModel):
    access_token: str
    token_type: str


class OperationDTO(BaseModel):
    success: bool
    message: str
