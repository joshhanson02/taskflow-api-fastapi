from sqlalchemy.orm import Session  # Tạo phiên làm việc với db
from models.user_model import User  # Thao tác với class User
# Model for stored refresh tokens
from models.user_model import RefreshToken
# Lấy cách thức get_user_by_email và create_user để thao tác với database
from repositories.user_repository import (
    get_user_by_email, create_user, find_refresh_token, delete_refresh_token)
# Lấy hash_password, verify_password và create_access_token trong core/security
from core.security import (
    hash_password, verify_password, create_access_token, create_refresh_token, verify_refresh_token)
from exceptions.auth_exception import AuthException
import logging

logger = logging.getLogger(__name__)


def register_user(db: Session, username: str, email: str, password: str):
    try:
        # Logic đăng ký user
        logger.info(
            f"Registration attempt for email: {email}"
        )
        existing_user = get_user_by_email(db, email)
        if existing_user:
            logger.warning(
                f"Registration failed - email already exists: {email}"
            )
            raise AuthException(
                status_code=400,
                detail="Email already registered"
            )
        hashed_password = hash_password(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        created_user = create_user(db, new_user)

        logger.info(
            f"User registered successfully with ID {created_user.id}"
        )
        return created_user
    except Exception as e:
        logger.error(f"Registration error for {email}: {str(e)}")
        raise


def login_user(db: Session, identifier, password):
    try:
        # logic đăng nhập
        # Gọi get_user_by_email bên user_repository
        logger.info(
            f"Login attempt for email: {identifier}"
        )
        user = get_user_by_email(db, identifier)
        if not user:
            logger.warning(
                f"Login failed - user not found: {identifier}"
            )
            raise AuthException(
                status_code=401,
                detail="Invalid email or password"
            )

        # tạo biến để lưu kết quả so sánh giữa password trong database và password được nhập vào bởi client
        valid_password = verify_password(password, user.password)
        if not valid_password:
            logger.warning(
                f"Login failed - invalid password for: {identifier}"
            )
            raise AuthException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        refresh_token = create_refresh_token(
            data={"sub": str(user.id)}
        )

        logger.info(
            f"User {user.id} logged in successfully"
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    except Exception:
        logger.error(f"Login error for {identifier}")
        raise


def refresh_access_token(db: Session, refresh_token: str):
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise AuthException(
            status_code=401,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")
    stored_token = find_refresh_token(db, refresh_token)
    if not stored_token:
        raise AuthException(
            status_code=401,
            detail="Refresh token revoked"
        )
    new_access_token = create_access_token(
        {
            "sub": user_id
        }
    )
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


def logout_user(db: Session, refresh_token: str):
    try:
        stored_token = find_refresh_token(db, refresh_token)
    except Exception:
        raise AuthException(
            status_code=404,
            detail="Token not found"
        )
    return delete_refresh_token(db, stored_token)
