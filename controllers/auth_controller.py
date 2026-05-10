from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from db.session import get_db

from schemas.auth_schema import (RegisterRequest, LoginRequest)

from services.auth_service import (register_user, login_user)

router = APIRouter()


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, request.username, request.email, request.password)
    if not user:
        return {
            "message": "Email already exists"
        }
    return {
        "message": "User created successfully"
    }


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    token = login_user(db, request.email, request.password)

    if not token:
        return {
            "message": "Invalid credentials"
        }
    return {
        "access_token": token,
        "token_type": "bearer"
    }
