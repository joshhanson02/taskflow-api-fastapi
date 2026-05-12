# Giả sử file bạn vừa gửi tên là security.py
from core.security import create_access_token, verify_token


def test_jwt_flow():
    # 1. Tạo dữ liệu giả (Payload mong muốn)
    raw_data = {
        "sub": "1234567890",
        "username": "hieu_admin",
        "role": "admin"
    }
    print(f"--- 1. Original Data ---\n{raw_data}\n")

    # 2. Tạo Token
    token = create_access_token(data=raw_data)
    print(f"--- 2. Encoded JWT (Gửi cái này cho client) ---\n{token}\n")

    # 3. Giải mã Token (Verify) để xem Payload
    decoded_payload = verify_token(token)

    if decoded_payload:
        print(f"--- 3. Decoded Payload (Dữ liệu bên trong) ---")
        print(f"User ID (sub): {decoded_payload.get('sub')}")
        print(f"Username: {decoded_payload.get('username')}")
        # Đây là Unix timestamp
        print(f"Expires (exp): {decoded_payload.get('exp')}")

        # Thử in toàn bộ payload ra xem
        print(f"\nFull Payload dict: {decoded_payload}")
    else:
        print("Token không hợp lệ hoặc đã hết hạn!")


if __name__ == "__main__":
    test_jwt_flow()
