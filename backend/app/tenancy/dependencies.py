from fastapi import HTTPException, status

from app.tenancy.tenant import get_current_tenant


async def resolve_tenant():
    tenant = get_current_tenant()
    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant information missing in token"
        )
    return tenant

