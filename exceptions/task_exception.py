from fastapi import HTTPException, status


class TaskException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(
            status_code=status_code,
            detail=detail
        )


class TaskNotFoundException(TaskException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            "Task not found"
        )


class ForbiddenException(TaskException):
    def __init__(self):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            "Forbidden"
        )
