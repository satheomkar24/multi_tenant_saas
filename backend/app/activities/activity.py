from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

from app.enums.activity import ActivityAction
from app.enums.user import Role

class Activity(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    tenant_id: str = Field(...)
    actor_id: str = Field(...)
    actor_role: Role = Field(...)
    action: ActivityAction = Field(...)
    entity: str = Field(...)
    entity_id: str = Field(...)
    message: str
    meta: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


