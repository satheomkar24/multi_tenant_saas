from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status

from app.core.password import hash_password
from app.enums.user import Role
from app.providers.repository import get_user_repo
from app.users.repository import UserRepository
from app.users.type import CreateUserRequest


async def get_all_users():
    userRepository = get_user_repo()
    users = await userRepository.find_all()
    return users


async def create_user(data: CreateUserRequest, tenant_id):
    userRepository = get_user_repo()
    if await userRepository.exists({"email": data.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    user = {
        "email": data.email,
        "password": hash_password(data.password),
        "tenant_id": tenant_id,
        "role": Role.USER,
        "is_active": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    await userRepository.insert_one(user)


async def delete_user_by_id(user_id: ObjectId, tenant_id):
    user_repo = get_user_repo()
    result = await user_repo.delete_one(
        {
            "_id": user_id,
            "tenant_id": tenant_id,
        }
    )
    if not result.deleted_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
