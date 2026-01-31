from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import Collections


class TenantRepository():
  def __init__(self, db: AsyncIOMotorDatabase):
    self.collection = db.get_collection(Collections.TENANTS)


  async def find_one(self, data: dict ):
    return await self.collection.find_one(data)
  
  
  async def insert_one(self, data: dict):
    return await self.collection.insert_one(data)
    

