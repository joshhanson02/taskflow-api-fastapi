from fastapi import (APIRouter, Depends)
from sqlalchemy.orm import Session
from db.session import get_db
from dependencies.auth_dependency import get_current_user
from schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from services.task_service import create_new_task, get_user_tasks, update_user_task, delete_user_task

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "",
    response_model=TaskResponse
)
def create_task(
    request: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return create_new_task(
        db=db,
        task_data=request,
        current_user=current_user
    )


@router.get(
    "",
    response_model=list[TaskResponse]
)
def get_tasks(
    status: str | None = None,
    priority: str | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_user_tasks(
        db=db,
        current_user=current_user,
        status=status,
        priority=priority,
        search=search,
        skip=skip,
        limit=limit
    )
