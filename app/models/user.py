from datetime import datetime
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    name: str = Field(..., example="Johan Sebastian")
    last_name: str = Field(..., example="Cañon")

class UserCreate(UserBase):
    password: str = Field(..., example="password123")

class UserInDB(UserBase):
    id: str
    username: str
    hashed_password: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id: str
    username: str
    created_at: datetime

class UserLogin(BaseModel):
    username: str = Field(..., example="johan.canon")
    password: str = Field(..., example="password123")
