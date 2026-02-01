from fastapi import HTTPException, status
from app.activities.service import create_activity
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.core.password import hash_password, verify_password
from app.enums.activity import ActivityAction
from app.enums.user import Role
from app.providers.repository import get_tenant_repo, get_user_repo
from app.users.user import User


async def signup_tenant_admin(name, slug, email: str, password):
    tenantRepository = get_tenant_repo()
    userRepository = get_user_repo()

    tenant_data = {"name": name, "slug": slug, "is_active": False}

    tenant_result = await tenantRepository.insert_one(tenant_data)
    tenant_id = str(tenant_result.inserted_id)

    user_data = {
        "email": email.lower(),
        "password": hash_password(password),
        "tenant_id": tenant_id,
        "role": Role.ADMIN,
        "is_active": False,
    }

    user_result = await userRepository.insert_one(user_data)
    user_data["_id"] = str(user_result.inserted_id)
    user_data["tenant_id"] = tenant_id

    created_user = {**user_data, "id": str(user_result.inserted_id)}

    await create_activity(
        action=ActivityAction.USER_CREATED,
        entity="user",
        entity_id=user_result.inserted_id,
        message=f"User {user_data['email']} created",
        meta={"role": user_data["role"]},
        user=User(**created_user),
    )

    return {"tenant": tenant_data, "user": user_data}


async def login_user(email, password, tenant_slug):
    tenantRepository = get_tenant_repo()
    userRepository = get_user_repo()

    tenant = await tenantRepository.find_one({"slug": tenant_slug, "is_active": True})
    if not tenant:
        raise ValueError("Tenant not found")
    tenant_id = str(tenant["_id"])

    user = await userRepository.find_one(
        {"email": email, "tenant_id": tenant_id, "is_active": True}
    )

    if not user or not verify_password(password, user["password"]):
        raise ValueError("Invalid credentials")

    token_payload = {
        "tenant_id": tenant_id,
        "tenant_slug": tenant["slug"],
        "user_id": str(user["_id"]),
        "role": user["role"],
    }

    # Create new access token
    new_access_token = create_access_token(token_payload)

    # Create new refresh token (refresh token rotation)
    new_refresh_token = create_refresh_token(token_payload)

    return {
        "role": user["role"],
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
    }


async def createNewTokens(refresh_token: str):
    # decode and validate refresh token
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
        )

    user_id = payload.get("user_id")
    tenant_id = payload.get("tenant_id")
    tenant_slug = payload.get("tenant_slug")
    role = payload.get("role")

    if not all([user_id, tenant_id, role, tenant_slug]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    token_payload = {
        "user_id": user_id,
        "tenant_id": tenant_id,
        "tenant_slug": tenant_slug,
        "role": role,
    }

    # Create new access token
    new_access_token = create_access_token(token_payload)

    # Create new refresh token (refresh token rotation)
    new_refresh_token = create_refresh_token(token_payload)

    return {"access_token": new_access_token, "refresh_token": new_refresh_token}
