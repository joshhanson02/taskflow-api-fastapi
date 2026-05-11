from pydantic import BaseModel, Field
from pydantic import EmailStr  # Dùng để xác thực form email


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=6)
# Create class to validate data input


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
