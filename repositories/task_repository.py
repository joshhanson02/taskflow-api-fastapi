from models.task_model import Task
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from exceptions.task_exception import TaskNotFoundException


def create_task(db: Session, request, current_user):
    task = Task(
        title=request.title,
        description=request.description,
        status=request.status,
        priority=request.priority,
        due_date=request.due_date,
        owner_id=current_user.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(
    db: Session,
    owner_id: int,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):

    query = db.query(Task).filter(Task.owner_id == owner_id)

    if status:
        query = query.filter(Task.status == status)

    if priority:
        query = query.filter(Task.priority == priority)

    if search:
      # or_ là xét điều kiện 1 trong 2
        query = query.filter(or_(
            Task.title.ilike(f"%{search}%"),
            Task.description.ilike(f"%{search}%")
        ))

    if not query:
        raise TaskNotFoundException()

    query = query.order_by(Task.updated_at.desc())
    return query.offset(skip).limit(limit).all()


def get_task_by_id(db: Session, task_id: int):
    return (db.query(Task).filter(Task.id == task_id).first())


def update_task(db: Session, task: Task, update_data):
    for key, value in update_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
