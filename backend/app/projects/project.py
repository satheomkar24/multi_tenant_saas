from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

class Project(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    tenant_id: str
    name: str
    description: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
