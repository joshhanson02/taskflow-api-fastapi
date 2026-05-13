from exceptions.task_exception import TaskNotFoundException, ForbiddenException
from repositories.task_repository import create_task, get_task_by_id, get_tasks, update_task, delete_task


def create_new_task(db, task_data, current_user):
    return create_task(
        db=db,
        task_data=task_data,
        owner_id=current_user.id
    )


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


def update_user_task(db, task_id, task_data, current_user):
    task = get_task_by_id(db, task_id)

    if not task:
        raise TaskNotFoundException()

    if task.owner_id != current_user.id:
        raise ForbiddenException()

    return update_task(db, task, task_data)


def delete_user_task(db, task_id, current_user):
    task = get_task_by_id(db, task_id)
    if not task:
        raise TaskNotFoundException()

    if task.owner_id != current_user.id:
        raise ForbiddenException()

    return delete_task(db, task)
