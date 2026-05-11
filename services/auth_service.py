from sqlalchemy.orm import Session  # Tạo phiên làm việc với db
from models.user_model import User  # Thao tác với class User
# Lấy cách thức get_user_by_email và create_user để thao tác với database
from repositories.user_repository import (get_user_by_email, create_user)
# Lấy hash_password, verify_password và create_access_token trong core/security
from core.security import (hash_password, verify_password, create_access_token)


def register_user(db: Session, username: str, email: str, password: str):
  # Logic đăng ký user
    existing_user = get_user_by_email(db, email)
    if existing_user:
        return None
    hashed_password = hash_password(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    return create_user(db, new_user)


def login_user(db: Session, identifier, password):
  # logic đăng nhập
    # Gọi get_user_by_email bên user_repository
    user = get_user_by_email(db, identifier)
    if not user:
        return None

    # tạo biến để lưu kết quả so sánh giữa password trong database và password được nhập vào bởi client
    valid_password = verify_password(password, user.password)
    if not valid_password:
        return None

    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )

    return access_token
