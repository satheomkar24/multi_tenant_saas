from fastapi import APIRouter, HTTPException, status
from jose import ExpiredSignatureError
from pydantic import BaseModel, EmailStr
from app.auth.service import (
  createNewTokens,
  login_user,
  signup_tenant_admin,
)
from app.core.jwt import create_access_token, create_refresh_token, decode_token


router = APIRouter(prefix="/auth", tags=["Auth"])


class SignupRequest(BaseModel):
  email: EmailStr
  password: str
  tenant_name: str
  tenant_slug: str


class LoginRequest(BaseModel):
  email: EmailStr
  password: str
  tenant_slug: str


class RefreshRequest(BaseModel):
  refresh_token: str


@router.post("/signup")
async def signup(data: SignupRequest):
  try:
    result = await signup_tenant_admin(data.tenant_name, data.tenant_slug, data.email, data.password)
    return {"success": True, "tenant": result["tenant"], "user": result["user"]}
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login")
async def login(data: LoginRequest):
  try:
    user = await login_user(data.email, data.password, data.tenant_slug)
    access_token = create_access_token({"user_id": user["id"], "tenant_id": user["tenant_id"], "role": user["role"]})
    refresh_token = create_refresh_token({"user_id": user["id"], "tenant_id": user["tenant_id"], "role": user["role"]})
    return {"success": True, "user": user, "access_token": access_token, "refresh_token": refresh_token}
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh")
async def refresh_token(request: RefreshRequest):
  try:
    tokens = createNewTokens(request.refresh_token)
    return tokens
  except ExpiredSignatureError:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token expired"
    )
  except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=str(e)
    )
