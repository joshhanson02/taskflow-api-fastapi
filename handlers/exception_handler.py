from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.auth_exception import AuthException


async def auth_exception_handler(
    _request: Request,
    exc: AuthException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )
