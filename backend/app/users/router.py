from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr

from app.tenancy.dependencies import resolve_tenant
from app.core.database import get_database

router = APIRouter(prefix="/users", tags=["Users"])


class CreateUserRequest(BaseModel):
  email: EmailStr
  name: str


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
  data: CreateUserRequest,
  _ = Depends(resolve_tenant)
):
  db = get_database()

  user = {
    "email": data.email,
    "name": data.name,
    "tenant_id": db.tenant_id
  }

  await db.users.insert_one(user)

  return {
    "message": "User created",
    "email": data.email
  }
