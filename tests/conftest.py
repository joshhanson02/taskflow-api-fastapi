# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from main import app
from db.database import SessionLocal, engine
from models.user_model import Base  # Giả sử bạn dùng Base = declarative_base()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Tự động tạo bảng trước khi test và xóa bảng sau khi test xong"""
    # Base.metadata.create_all(bind=engine) # Mở ra nếu muốn tự tạo bảng ảo khi test
    yield
    # Base.metadata.drop_all(bind=engine)  # Dọn dẹp sau khi test xong (nếu dùng DB test riêng)


@pytest.fixture(scope="function")
def db_session():
    """Fixture cung cấp DB Session sạch cho mỗi hàm test, tự rollback để tránh lệch dữ liệu"""
    session = SessionLocal()
    yield session
    session.rollback()  # Đảm bảo không làm thay đổi DB thật sau khi test xong
    session.close()


@pytest.fixture(scope="module")
def client():
    """Fixture cung cấp TestClient cho toàn bộ các file test API"""
    with TestClient(app) as c:
        yield c
