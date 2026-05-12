from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.auth_schema import RegisterRequest, UserResponse, TokenResponse
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import (register_user, login_user)
from dependencies.auth_dependency import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, request.username, request.email, request.password)
    if not user:
        return {
            "message": "Email already exists"
        }
    return {
        "message": "User created successfully"
    }


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = login_user(db, form_data.username, form_data.password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
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
