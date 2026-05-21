# tests/test_auth.py
import pytest
from core.security import create_access_token, verify_token


def test_jwt_flow():
    raw_data = {
        "sub": "1234567890",
        "username": "hieu_admin",
        "role": "admin"
    }

    # 1. Test tạo token
    token = create_access_token(data=raw_data)
    assert token is not None
    assert isinstance(token, str)

    # 2. Test giải mã và verify token
    decoded_payload = verify_token(token)
    assert decoded_payload is not None
    assert decoded_payload.get("sub") == "1234567890"
    assert decoded_payload.get("username") == "hieu_admin"
    assert "exp" in decoded_payload
