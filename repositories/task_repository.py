from models.task_model import Task
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional


def create_task(db: Session, task_data, owner_id: int):
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        owner_id=owner_id
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
    query = db.query(Task)

    query = query.filter(Task.owner_id == owner_id)

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

    query = query.offset(skip).limit(limit)
    return query.all()


def get_task_by_id(db: Session, task_id: int):
    return (db.query(Task).filter(Task.id == task_id).first())


def update_task(db: Session, task: Task, task_data):
    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status
    task.priority = task_data.priority

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
