from sqlalchemy.orm import Session
from models.user_model import User

# dùng để lấy user thông qua email


def get_user_by_email(db: Session, email: str):
    return (db.query(User).filter(User.email == email).first())
  # Trả về giá trị user bằng cách lọc so sánh email trong database với email nhập vào có giống nhau không, nếu giống thì trả về user đã tìm thấy


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
