from fastapi import APIRouter, Depends, status

from app.enums.user import Role
from app.tenancy.dependencies import allow_roles, resolve_tenant
from app.core.database import get_database
from app.users.service import create_user, delete_user_by_id, get_all_users
from app.users.type import CreateUserRequest
from app.users.user import User
from app.utils.object_id import to_object_id


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def get_all(_=Depends(resolve_tenant)):
    users = await get_all_users()
    return users


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    payload: CreateUserRequest, user: User = Depends(allow_roles(Role.ADMIN))
):
    await create_user(payload, user.tenant_id)
    return {"message": "User created Successfully."}


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    user_id: str,
    current_user: User = Depends(allow_roles(Role.ADMIN)),
):
    user_oid = to_object_id(user_id, "user_id")
    await delete_user_by_id(
        user_id=user_oid,
        tenant_id=current_user.tenant_id,
    )
