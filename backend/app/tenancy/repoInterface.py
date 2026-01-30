from abc import ABC, abstractmethod


class TenantRepositoryInterface(ABC):

  @abstractmethod
  async def find_one(self, data: dict ):
    pass
  
  @abstractmethod
  async def insert_one(self, data: dict):
    pass


