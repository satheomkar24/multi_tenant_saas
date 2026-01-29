from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.jwt import decode_token
from app.tenancy.tenant import Tenant, set_current_tenant

security = HTTPBearer()

async def resolve_tenant(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    payload = decode_token(token)

    tenant_id = payload.get("tenant_id")
    tenant_slug = payload.get("tenant_slug")

    if not tenant_id or not tenant_slug:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant information missing in token"
        )

    # validate tenant exists in DB
    tenant = Tenant(
        id=tenant_id,
        slug=tenant_slug,
        name=tenant_slug.capitalize()
    )

    set_current_tenant(tenant)

    return tenant
