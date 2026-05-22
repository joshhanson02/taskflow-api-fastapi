from sqlalchemy.orm import Session
from models.user_model import User
from models.user_model import RefreshToken
# dùng để lấy user thông qua email


def get_user_by_email(db: Session, identifier):
    return (db.query(User).filter(User.email == identifier).first())
  # Trả về giá trị user bằng cách lọc so sánh email trong database với email nhập vào có giống nhau không, nếu giống thì trả về user đã tìm thấy


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def find_refresh_token(db: Session, token: str):
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()


def delete_refresh_token(db: Session, token: str):
    db.query(RefreshToken).filter(RefreshToken.token == token).delete()
    db.commit()
    return {"message": "Logout successful"}
