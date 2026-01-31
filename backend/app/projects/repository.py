from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import Collections


class ProjectRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection(Collections.PROJECTS)

    async def find_all(self):
        return await self.collection.find().to_list()

    async def find(self, data: dict):
        return await self.collection.find(data).to_list()

    async def find_one(self, data: dict):
        return await self.collection.find_one(data)

    async def insert_one(self, data: dict):
        return await self.collection.insert_one(data)

    async def exists(self, query: dict) -> bool:
        return await self.collection.find_one(query, {"_id": 1}) is not None

    async def update_one(self, data: dict, project_id: ObjectId, tenant_id: ObjectId):
        return await self.collection.update_one(
            {"_id": project_id, "tenant_id": tenant_id},
            {"$set": data},
        )

    async def delete_one(self, query: dict):
        return await self.collection.delete_one(query)
