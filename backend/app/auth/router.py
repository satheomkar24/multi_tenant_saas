from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.auth.service import (
  hash_password,
  verify_password,
  create_access_token
)


router = APIRouter(prefix="/auth", tags=["Auth"])


class SignupRequest(BaseModel):
  email: EmailStr
  password: str
  tenant_name: str
  tenant_slug: str


class LoginRequest(BaseModel):
  email: EmailStr
  password: str


@router.post("/signup")
async def signup(data: SignupRequest):
  # 🔴 TODO: check tenant uniqueness in DB
  # 🔴 TODO: save tenant
  # 🔴 TODO: save user with tenant_id

  tenant_id = "tenant_generated_id"
  user_id = "user_generated_id"

  hashed = hash_password(data.password)

  token = create_access_token(
    user_id=user_id,
    tenant_id=tenant_id,
    tenant_slug=data.tenant_slug
  )

  return {
    "access_token": token,
    "token_type": "bearer"
  }


@router.post("/login")
async def login(data: LoginRequest):
  # 🔴 TODO: fetch user by email
  # 🔴 TODO: verify password
  # 🔴 TODO: get tenant from user

  fake_hashed_password = hash_password("password")

  if not verify_password(data.password, fake_hashed_password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid credentials"
    )

  user_id = "user_id"
  tenant_id = "tenant_id"
  tenant_slug = "acme"

  token = create_access_token(
    user_id=user_id,
    tenant_id=tenant_id,
    tenant_slug=tenant_slug
  )

  return {
    "access_token": token,
    "token_type": "bearer"
  }
