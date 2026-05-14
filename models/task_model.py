from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db.database import Base
from schemas.task_schema import TaskStatus, TaskPriority


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.pending)
    priority = Column(SQLAlchemyEnum(TaskPriority),
                      default=TaskPriority.medium)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    due_date = Column(
        DateTime(timezone=True),
        nullable=True
    )
    owner = relationship("User", back_populates="tasks")
