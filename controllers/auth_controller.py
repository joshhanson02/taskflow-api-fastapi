from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.auth_schema import RegisterRequest, UserResponse, TokenResponse, RefreshTokenResponse, RefreshTokenRequest, LogoutRequest
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import (
    register_user, login_user, refresh_access_token, logout_user)
from dependencies.auth_dependency import get_current_user
from exceptions.auth_exception import EmailAlreadyExistsException, InvalidCredentialsException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=UserResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, request.username, request.email, request.password)
    if not user:
        raise EmailAlreadyExistsException()
    return user


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    tokens = login_user(
        db, form_data.username, form_data.password)

    if not tokens:
        raise InvalidCredentialsException()
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["access_token"],
        "token_type": "bearer"
    }


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse
)
def refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    return refresh_access_token(
        db,
        request.refresh_token
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout(
    request: LogoutRequest,
    db: Session = Depends(get_db)
):
    return logout_user(
        db,
        request.refresh_token
    )
