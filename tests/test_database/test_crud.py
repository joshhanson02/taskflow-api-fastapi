# tests/test_database/test_crud.py
from models.user_model import User


def test_insert_and_query_user(db_session):
    # 1. DỌN DẸP TRƯỚC: Xóa user test cũ nếu lỡ có từ lần chạy trước
    db_session.query(User).filter(
        User.email == "trunghieuidol02@gmail.com").delete()
    db_session.commit()

    # 2. TIẾN HÀNH TEST: Tạo mới bình thường
    new_user = User(
        username="hieu",
        email="trunghieuidol02@gmail.com",
        password="hashed_password_123"
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    # 3. Query lại để assert
    user_in_db = db_session.query(User).filter(
        User.email == "trunghieuidol02@gmail.com").first()
    assert user_in_db is not None
    assert user_in_db.username == "hieu"


def test_update_user(db_session):
    # Giả sử đã có user (hoặc tạo nhanh 1 user để test)
    user = db_session.query(User).first()
    if user:
        original_name = user.username
        user.username = "new_name"
        db_session.commit()

        # Query lại xem đã đổi chưa
        db_session.refresh(user)
        assert user.username == "new_name"


def test_delete_user(db_session):
    user = db_session.query(User).first()
    if user:
        db_session.delete(user)
        db_session.commit()

        # Check lại xem còn tồn tại không
        check_user = db_session.query(User).filter(User.id == user.id).first()
        assert check_user is None
