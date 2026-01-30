
from app.core.database import get_database
from app.tenancy.repository import TenantRepository
from app.users.repository import UserRepository


def get_tenant_repo() -> TenantRepository:
  return TenantRepository(get_database())


def get_user_repo() -> UserRepository:
  return UserRepository(get_database())