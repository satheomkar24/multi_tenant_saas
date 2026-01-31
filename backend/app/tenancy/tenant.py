from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from contextvars import ContextVar


class Tenant(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    slug: str
    name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


_current_tenant: ContextVar[Tenant | None] = ContextVar(
    "current_tenant",
    default=None
)

def set_current_tenant(tenant: Tenant) -> None:
    _current_tenant.set(tenant)

def get_current_tenant() -> Tenant:
    tenant = _current_tenant.get()
    if tenant is None:
        raise RuntimeError("Tenant not set in request context")
    assert tenant is not None
    return tenant
