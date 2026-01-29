from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3


def hash_password(password: str) -> str:
  return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
  *,
  user_id: str,
  tenant_id: str,
  tenant_slug: str
) -> str:
  expire = datetime.now() + timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
  )

  payload = {
    "sub": user_id,
    "tenant_id": tenant_id,
    "tenant_slug": tenant_slug,
    "exp": expire
  }

  token = jwt.encode(
    payload,
    settings.JWT_SECRET,
    algorithm=ALGORITHM
  )
  return token
