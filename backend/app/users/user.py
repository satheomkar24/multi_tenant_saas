from contextvars import ContextVar
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId
from app.enums.user import Role


class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: EmailStr
    password: str
    tenant_id: str
    role: Role = Role.USER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


_current_user: ContextVar[User | None] = ContextVar("current_user", default=None)


def set_current_user(user: User) -> None:
    _current_user.set(user)


def get_current_user() -> User:
    user = _current_user.get()
    if user is None:
        raise RuntimeError("User not set in request context")
    assert user is not None
    return user
