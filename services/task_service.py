from exceptions.task_exception import TaskNotFoundException, ForbiddenException
from repositories.task_repository import create_task, get_task_by_id, get_tasks, update_task, delete_task
from models.task_model import Task
from core.logger import logger


def create_new_task(db, request, current_user):
    try:
        logger.info(
            f"User {current_user.id} is creating a task"
        )
        task = create_task(
            db,
            request,
            current_user
        )

        logger.info(
            f"Task {task.id} created successfully"
        )
        return task
    except Exception as e:
        logger.error(
            f"Task creation failed for user "
            f"{current_user.id}: {str(e)}"
        )
        raise


def get_user_tasks(db, current_user, status=None, priority=None, search=None, skip=0, limit=10):
    logger.info(f"User {current_user.id} fetched tasks")
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
    try:
        logger.info(
            f"User {current_user.id} "
            f"is updating task {task_id}"
        )
        task = get_task_by_id(db, task_id)

        if not task:
            logger.warning(
                f"Task {task_id} not found"
            )
            raise TaskNotFoundException()

        if task.owner_id != current_user.id:
            logger.warning(
                f"User {current_user.id} attempted "
                f"unauthorized update on task {task_id}"
            )
            raise ForbiddenException()

        logger.info(f"Task {task_id} updated successfully")
        return update_task(db, task, request)

    except Exception as e:
        logger.error(
            f"Task update failed for "
            f"task {task_id}: {str(e)}"
        )
        raise


def delete_user_task(db, task_id, current_user):
    try:
        logger.warning(
            f"User {current_user.id} "
            f"is deleting task {task_id}"
        )
        task = get_task_by_id(db, task_id)
        if not task:
            logger.warning(
                f"Task {task_id} not found"
            )
            raise TaskNotFoundException()

        if task.owner_id != current_user.id:
            logger.warning(
                f"User {current_user.id} attempted "
                f"unauthorized delete on task {task_id}"
            )
            raise ForbiddenException()

        delete_task(db, task)
        logger.warning(
            f"Task {task_id} deleted successfully"
        )

    except Exception as e:
        logger.error(
            f"Task deletion failed for "
            f"task {task_id}: {str(e)}"
        )
        raise
