from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class BaseRepository:
  def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
    self.collection = db.get_collection(collection_name)


  async def find_all(
      self,
      query: dict | None = None,
      *,
      limit: int | None = None,
      sort: tuple[str, int] | None = None
  ):
    query = query or {}
    cursor = self.collection.find(query)

    if sort is not None and len(sort) == 2:
      field, direction = sort
      cursor = cursor.sort(field, direction)

    return await cursor.to_list(length=limit)
  

  async def find_one(self, query: dict):
    return await self.collection.find_one(query)
  

  async def exists(self, query: dict) -> bool:
    return await self.collection.find_one(query, {"_id": 1}) is not None


  async def insert_one(self, data: dict):
    now = datetime.now()
    data.setdefault("created_at", now)
    data.setdefault("updated_at", now)
    return await self.collection.insert_one(data)


  async def update_one(
      self,
      *,
      id: ObjectId,
      tenant_id: ObjectId,
      data: dict
  ):
    data["updated_at"] = datetime.now()
    return await self.collection.update_one(
      {"_id": id, "tenant_id": tenant_id},
      {"$set": data}
    )


  async def delete_one(self, query: dict):
    return await self.collection.delete_one(query)
