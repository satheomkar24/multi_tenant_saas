from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
  email: EmailStr
  name: str
  password: str