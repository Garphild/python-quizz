from pydantic import BaseModel, Field
from typing import Annotated

"""
Login DTOs
"""
class LoginRequestDto(BaseModel):
    email: Annotated[str, Field(description="User email", example="user@example.com")]
    password: Annotated[str, Field(description="User password", example="password123")]

"""
Register DTOs
"""
class RegisterRequestDto(BaseModel):
    email: Annotated[str, Field(description="User email", example="user@example.com")]
    password: Annotated[str, Field(description="User password", example="password123")]
    name: Annotated[str, Field(description="User name", example="John")]
    surname: Annotated[str | None, Field(description="User surname", example="Doe")] = None

"""
Current User Profile DTOs
"""
class ProfileDto(BaseModel):
    id: Annotated[int, Field(description="User ID")]
    email: Annotated[str, Field(description="User email")]
    name: Annotated[str, Field(description="User name")]
    surname: Annotated[str | None, Field(description="User surname")] = None

"""
Update Current User Profile DTOs
"""
class UpdateProfileDto(BaseModel):
    name: Annotated[str | None, Field(description="User name")] = None
    surname: Annotated[str | None, Field(description="User surname")] = None

"""
Change Current User Password DTOs
"""
class ChangePasswordDto(BaseModel):
    old_password: Annotated[str, Field(description="Current password")]
    new_password: Annotated[str, Field(description="New password")]

