from typing import cast
from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.auth_exception import AuthException


async def auth_exception_handler(
    _request: Request,
    exc: Exception
):
    auth_exc = cast(AuthException, exc)
    return JSONResponse(
        status_code=auth_exc.status_code,
        content={
            "success": False,
            "error": auth_exc.detail
        }
    )
