from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Answer:
    id: int
    answer: str
    is_correct: bool

class AnswerEntity(Answer):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class AnswerDto(AnswerEntity, BaseModel):
    id: int