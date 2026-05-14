from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models.user_model import User
from core.security import verify_token
from fastapi.security import OAuth2PasswordBearer
from exceptions.auth_exception import InvalidTokenException, UserNotFoundException, PermissionDeniedException, InvalidCredentialsException
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        raise InvalidTokenException()

    email = payload.get("sub")
    if email is None:
        raise InvalidCredentialsException()

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise UserNotFoundException()

    return user


def require_role(required_role: str):
    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if str(current_user.role) != required_role:
            raise PermissionDeniedException()
        return current_user
    return role_checker
