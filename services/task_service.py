from exceptions.task_exception import TaskNotFoundException, ForbiddenException
from repositories.task_repository import create_task, get_task_by_id, get_tasks, update_task, delete_task
from models.task_model import Task


def create_new_task(db, request, current_user):
    return create_task(db, request, current_user)


def get_user_tasks(db, current_user, status=None, priority=None, search=None, skip=0, limit=10):
    return get_tasks(
        db=db,
        owner_id=current_user.id,
        status=status,
        priority=priority,
        search=search,
        skip=skip,
        limit=limit
    )


def update_user_task(db, task_id, request, current_user):
    task = get_task_by_id(db, task_id)

    if not task:
        raise TaskNotFoundException()

    if task.owner_id != current_user.id:
        raise ForbiddenException()

    update_task = request.model_dump(exclude_unset=True)

    return update_task(db, task, request)


def delete_user_task(db, task_id, current_user):
    task = get_task_by_id(db, task_id)
    if not task:
        raise TaskNotFoundException()

    if task.owner_id != current_user.id:
        raise ForbiddenException()

    return delete_task(db, task)
