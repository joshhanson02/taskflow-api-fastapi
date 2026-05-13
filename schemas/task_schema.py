from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: Optional[str] = None
    priority: Optional[str] = "medium"


class TaskUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    priority: str


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
