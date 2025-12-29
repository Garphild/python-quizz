from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Question:
    id: int
    question: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
class QuestionEntity(Question):
    pass

class QuestionDto(BaseModel):
    id: int
    question: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None