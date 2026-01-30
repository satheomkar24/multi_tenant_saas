from bson import ObjectId
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, status

from app.core.jwt import decode_token
from app.providers.repository import get_tenant_repo
from app.tenancy.tenant import set_current_tenant


class TenantMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")

        # Allow public routes
        if not auth_header:
            return await call_next(request)

        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Authorization header"
            )

        token = auth_header.split(" ")[1]

        payload = decode_token(token)

        tenant_id = payload.get("tenant_id")
        tenant_slug = payload.get("tenant_slug")

        if not tenant_id or not tenant_slug:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tenant information missing in token"
            )

        # validate tenant from DB / cache
        tenantRepository = get_tenant_repo()
        tenant = await tenantRepository.find_one({"_id": ObjectId(tenant_id), "slug": tenant_slug, "is_active": True})
        if not tenant:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Tenant not found or inactive"
          )

        # SET CONTEXT
        set_current_tenant(tenant)

        # Continue request
        response = await call_next(request)

        return response
