from fastapi import HTTPException, status


class AuthException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(
            status_code=status_code,
            detail=detail
        )


class InvalidTokenException(AuthException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid token"
        )


class UserNotFoundException(AuthException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "User not found"
        )


class EmailAlreadyExistsException(AuthException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            "Email already exists"
        )


class PermissionDeniedException(AuthException):
    def __init__(self):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            "Permission denied"
        )


class InvalidCredentialsException(AuthException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid credentials",
        )
