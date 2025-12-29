from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field

class PublicUser(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class UserEntity(PublicUser):
    password: str

class PublicUserDto(BaseModel):
    id: Annotated[int, Field(description="User identifier")]
    name: Annotated[str, Field(description="User's first name")]
    surname: Annotated[str, Field(description="User's last name")]
    email: Annotated[str, Field(description="User's email address")]

class UserCreateDto(BaseModel):
    name: Annotated[str, Field(description="User's first name")]
    surname: Annotated[str, Field(description="User's last name")]
    email: Annotated[str, Field(description="User's email address")]
    password: Annotated[str, Field(description="User's password")]

class UserLoginDto(BaseModel):
    email: Annotated[str, Field(description="User's email address")]
    password: Annotated[str, Field(description="User's password")]

class GoogleUserDto(BaseModel):
    email: Annotated[str, Field(description="User's email address")]
    name: Annotated[str, Field(description="User's first name")]
    surname: Annotated[str, Field(description="User's last name")]
    google_id: Annotated[str | None, Field(description="Google user ID", default=None)]
    avatar_url: Annotated[str | None, Field(description="User's avatar URL", default=None)]