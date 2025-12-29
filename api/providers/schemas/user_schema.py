from pydantic import BaseModel

from entities.user import UserEntity

class UserSchema(UserEntity, BaseModel):
    id: int

    class Config:
        orm_mode = True
