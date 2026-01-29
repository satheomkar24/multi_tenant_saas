from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
from app.tenancy.tenant import get_current_tenant

# Global variables to store client & database
mongo_client: AsyncIOMotorClient | None = None
mongo_db: AsyncIOMotorDatabase | None = None


async def connect_to_mongo():
  global mongo_client, mongo_db

  if mongo_client is None:
    mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
    mongo_db = mongo_client[settings.MONGO_DB_NAME]
    print("✅ MongoDB connected")


async def close_mongo_connection():
  global mongo_client, mongo_db

  if mongo_client:
    mongo_client.close()
    mongo_client = None
    mongo_db = None
    print("🛑 MongoDB disconnected")


def get_database() -> AsyncIOMotorDatabase:
  if mongo_db is None:
    raise RuntimeError("MongoDB client is not connected")

  # Attach tenant_id to db instance (request-safe)
  tenant = get_current_tenant()
  mongo_db.tenant_id = tenant.id  # type: ignore

  return mongo_db


async def init_collections():
    db= get_database()
    await db.tenants.create_index("slug", unique=True)
    await db.users.create_index([("email",1), ("tenant_id",1)], unique=True)
    await db.projects.create_index([("tenant_id",1)])
    await db.tasks.create_index([("tenant_id",1), ("project_id",1)])
    await db.activities.create_index([("tenant_id",1), ("user_id",1)])
