from fastapi import Depends, HTTPException, status

from app.enums.user import Role
from app.tenancy.tenant import get_current_tenant
from app.users.user import get_current_user


def resolve_tenant():
    tenant = get_current_tenant()
    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant information missing in token",
        )
    assert tenant is not None
    return tenant


def allow_roles(*allowed_roles: Role):
    async def role_checker():
        current_user = get_current_user()

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied, Insufficient permissions",
            )
        return current_user

    return role_checker
