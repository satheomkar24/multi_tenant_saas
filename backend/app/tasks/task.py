from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId
from app.enums.task import Priority, TaskStatus

class Task(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    tenant_id: str
    project_id: str
    title: str
    description: str
    assigned_to: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

