from sqlalchemy.orm import Session  # Tạo phiên làm việc với db
from models.user_model import User  # Thao tác với class User
# Lấy cách thức get_user_by_email và create_user để thao tác với database
from repositories.user_repository import (get_user_by_email, create_user)
# Lấy hash_password, verify_password và create_access_token trong core/security
from core.security import (hash_password, verify_password, create_access_token)
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
            data={
                "sub": user.email,
                "role": user.role
            }
        )

        logger.info(
            f"User {user.id} logged in successfully"
        )

        return access_token

    except Exception:
        logger.error(f"Login error for {identifier}")
        raise
