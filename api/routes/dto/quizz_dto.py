from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AdminQuizzDto(BaseModel):
    id: int
    name: str
    description: str
    questions_count: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class CreateQuizzDto(BaseModel):
    name: str
    description: str

class UpdateQuizzDto(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None