from bson import ObjectId
from fastapi import HTTPException, status


def to_object_id(
  value: str,
  field_name: str = "id",
) -> ObjectId:
  """
  Validate and convert string to MongoDB ObjectId
  """
  if not ObjectId.is_valid(value):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Invalid {field_name}",
    )
  
  return ObjectId(value)
