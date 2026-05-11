from passlib.context import CryptContext  # Dùng để hashing password
# CryptContext là một bộ quản lý manager từ thư viện passlib, giúp quản lý các thuật toán băm (hashing algorithms).
from jose import jwt  # Tạo JWT token hoặc encode/decode token
# dùng để lấy thời gian hiện tại và cộng thêm thời gian hết token
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv  # Dùng để đọc file .env
import os  # Cái này dùng để đọc biến môi trường
# 10/05/2026: Lưu ý cực mạnh, lỗi kinh điển khi test hash password là không khớp version
# passlib và bcrypt, passlib == 1.7.4 và bcrypt >= 4.1 không hợp nhau,
# cài lại thư viện bcrypt thành bản 4.0.1
load_dotenv()
# Lấy mấy cái giá trị trong file .env để dùng cho authentication
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:pass@localhost/db")  # Connect database
# Secret key là khoá bí mật để ký JWT
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_123")
# Cái này là thông tin thuật toán dùng để băm HMAC + SHA256
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))  # Thời gian sống của token

pwd_context = CryptContext(
    schemes=["bcrypt"],  # biểu hiện thuật toán muốn sử dụng để băm
    deprecated="auto"  # Tự động nhận diện thuật toán mới và cho những thuật toán cũ là lỗi thời,
    # Nếu password được hash bằng thuật toán cũ,
    # passlib vẫn verify được và hỗ trợ rehash sang thuật toán mới
)


def hash_password(password: str):
    return pwd_context.hash(password)
# Băm password gốc của user và trả về kết quả


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
# Xác thực mật khẩu bằng cách so sánh
# Khi user nhập mật khẩu ví dụ 123456 nó sẽ tự băm theo quy trình và so sánh password đã băm trong database


def create_access_token(data: dict):
    to_encode = data.copy()  # Dùng để copy dữ liệu, tránh sửa object gốc

    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Thời gian hiện tại + với thời gian hết hạn của token

    to_encode.update({"exp": expire})  # Thêm expiration vào payload JWT
    # Nó sẽ tự check exp trong payload của JWT để xem chừng nào hết hạn thì nó out

    # Secret key nó giống signature chữ ký, check xem có chuẩn không
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
  # trả về JWT đã mã hoá
