from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PublicUser:
    id: int
    name: str
    surname: str
    email: str

class UserEntity(PublicUser):
    password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class UserDto(UserEntity, BaseModel):
    id: int

class UserCreateDto(UserEntity, BaseModel):
    password: str

class UserLoginDto(BaseModel):
    email: str
    password: str

class GoogleUserDto(BaseModel):
    email: str
    name: str
    surname: str
    google_id: str
    avatar: str