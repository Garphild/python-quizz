from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field

class PublicUser(BaseModel):
    id: Annotated[int, Field(gt=0, description="User ID")]
    name: Annotated[str, Field(min_length=1, max_length=100, description="User name")]
    surname: Annotated[str, Field(min_length=1, max_length=100, description="User surname")]
    email: Annotated[str, Field(max_length=255, description="User email")]
    created_at: Annotated[Optional[datetime], Field(description="Creation timestamp")] = None
    updated_at: Annotated[Optional[datetime], Field(description="Last update timestamp")] = None
    deleted_at: Annotated[Optional[datetime], Field(description="Deletion timestamp")] = None

class User(BaseModel):
    password: Annotated[str, Field(min_length=1, description="User password")]

class UserEntity(User, PublicUser):
    class Config:
        from_attributes = True

