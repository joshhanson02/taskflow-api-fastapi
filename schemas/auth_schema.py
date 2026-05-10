from pydantic import BaseModel
from pydantic import EmailStr  # Dùng để xác thực form email


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
# Create class to validate data input


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
