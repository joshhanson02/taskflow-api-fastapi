from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.auth_exception import AuthException


async def auth_exception_handler(
    _request: Request,
    exc: Exception  # 1. Đổi thành Exception tổng quát để khớp cấu hình FastAPI
):
    # 2. Ép kiểu (Type Guard) giúp IDE nhận diện lại exc là AuthException
    if not isinstance(exc, AuthException):
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Internal Server Error"}
        )

    # 3. Các thuộc tính .status_code và .detail giờ đã an toàn và không bị báo lỗi
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )
