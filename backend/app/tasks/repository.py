from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import Collections
from app.providers.baseRepository import BaseRepository


class TaskRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, Collections.TASKS)
