from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import Collections
from app.users.repoInterface import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
  def __init__(self, db: AsyncIOMotorDatabase):
    self.collection = db.get_collection(Collections.USERS)


  async def find_one(self, data: dict ):
    return await self.collection.find_one(data)
  
  
  async def insert_one(self, data: dict):
    return await self.collection.insert_one(data)
    
