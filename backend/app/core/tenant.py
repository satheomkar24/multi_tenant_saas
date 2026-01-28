from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from app.core.config import settings


async def get_current_context(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        request.state.user_id = payload.get("sub")
        request.state.tenant_id = payload.get("tenant_id")
        request.state.role = payload.get("role")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return request.state
