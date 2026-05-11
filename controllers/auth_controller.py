from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.auth_schema import RegisterRequest
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import (register_user, login_user)
from dependencies.auth_dependency import get_current_user

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
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = login_user(db, form_data.username, form_data.password)

    if not token:
        return {
            "message": "Invalid credentials"
        }
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }
