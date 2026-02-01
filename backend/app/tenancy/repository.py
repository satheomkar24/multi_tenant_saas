from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import Collections
from app.providers.baseRepository import BaseRepository


class TenantRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, Collections.TENANTS)
