# tests/test_api/test_task.py
import pytest
from main import app
from dependencies.auth_dependency import get_current_user
from models.user_model import User


class MockUser:
    def __init__(self, id, username, email, role):
        self.id = id
        self.username = username
        self.email = email
        self.role = role


current_test_user = None


def mock_get_current_user():
    """Hàm Mock trả về đúng ID thật của User để ăn khớp với owner_id (Khóa ngoại)"""
    global current_test_user
    if current_test_user:
        return MockUser(
            id=current_test_user.id,
            username=current_test_user.username,
            email=current_test_user.email,
            role=current_test_user.role
        )

    return MockUser(id=1, username="hieu_api", email="hieu_test_api@gmail.com", role="user")


@pytest.fixture(scope="function", autouse=True)
def setup_api_test(db_session):
    """Fixture tự động dọn dẹp DB, tạo User thật và override bộ lọc Auth"""
    global current_test_user
    # 1. Dọn dẹp bản ghi cũ để tránh trùng Unique trùng lặp email
    db_session.query(User).filter(
        User.email == "hieu_test_api@gmail.com").delete()
    db_session.commit()

    # 2. Tạo User THẬT để sinh ID thật trong PostgreSQL kiểm thử
    user_record = User(
        username="hieu_api",
        email="hieu_test_api@gmail.com",
        password="hashed_password_123",
        role="user"
    )
    db_session.add(user_record)
    db_session.commit()
    db_session.refresh(user_record)
    current_test_user = user_record

    # 3. Ép FastAPI sử dụng quyền giả lập đã liên kết ID thật này
    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides.clear()


def test_health_check(client):
    """Test endpoint trạng thái hệ thống tại '/'"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome! The API is working now, you can test it by accessing the /docs directory."
    }


def test_create_task(client):
    """Test endpoint tạo mới một task thành công với dữ liệu chuẩn model"""
    payload = {
        "title": "Learn Pytest",
        "description": "Testing FastAPI project",
        "priority": "medium",  # Khớp với chữ thường mặc định trong Model của bạn
        "status": "pending"    # Khớp với chữ thường mặc định trong Model của bạn
    }

    response = client.post("/tasks/create_task", json=payload)
    # Chấp nhận cả 200 OK hoặc 201 Created tùy thuộc vào service của bạn viết
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data


def test_get_tasks(client):
    """Test endpoint lấy danh sách task thành công"""
    response = client.get("/tasks/get_tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
