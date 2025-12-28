from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from api.entities.answer import Answer

class Question:
    id: int
    question: str
    answers: Optional[list[Answer]] = None
    
class QuestionEntity(Question):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class QuestionDto(QuestionEntity, BaseModel):
    id: int