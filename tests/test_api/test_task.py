# tests/test_api/test_task.py
import pytest
from core.security import create_access_token
# Hãy đảm bảo đường dẫn import Model User này chính xác
from models.user_model import User


@pytest.fixture(scope="function")
def auth_headers(db_session):
    """Fixture tạo một User thật trong DB test và sinh Token tương ứng để vượt qua bộ lọc Auth"""
    # 1. Kiểm tra xem user test đã tồn tại chưa, nếu chưa thì insert vào DB
    test_user = db_session.query(User).filter(
        User.email == "hieu_test@gmail.com").first()
    if not test_user:
        test_user = User(
            username="hieu_test",
            email="hieu_test@gmail.com",
            password="hashed_password_123",  # Khớp với dữ liệu mã hóa của bạn nếu cần
            role="user"                      # Khớp với trường 'role' trong UserResponse
        )
        db_session.add(test_user)
        db_session.commit()
        db_session.refresh(test_user)

    # 2. Sử dụng ID thật vừa được sinh tự động từ DB để làm payload cho Token
    token_payload = {
        # JWT 'sub' nhận chuỗi string đại diện cho ID
        "sub": str(test_user.id),
        "username": test_user.username,
        "role": test_user.role
    }

    token = create_access_token(data=token_payload)
    return {"Authorization": f"Bearer {token}"}


def test_health_check(client):
    """Test endpoint trạng thái hệ thống tại '/'"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome! The API is working now, you can test it by accessing the /docs directory."
    }


def test_create_task(client, auth_headers):
    """Test endpoint tạo mới một task thành công với quyền đã được xác thực"""
    payload = {
        "title": "Learn Pytest",
        "description": "Testing FastAPI project",
        "priority": "HIGH",  # Điều chỉnh giá trị chuỗi này đúng với Enum TaskPriority của bạn
        "status": "TODO"     # Điều chỉnh giá trị chuỗi này đúng với Enum TaskStatus của bạn
    }

    response = client.post("/tasks/create_task",
                           json=payload, headers=auth_headers)

    # API thành công thường trả về 200 hoặc 201 Created
    assert response.status_code in [200, 201]

    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data


def test_get_tasks(client, auth_headers):
    """Test endpoint lấy danh sách task của user hiện tại"""
    response = client.get("/tasks/get_tasks", headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
