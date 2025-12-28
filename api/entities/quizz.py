from typing import Optional
from entities.questions import Question
from datetime import datetime
from pydantic import BaseModel

class Quizz:
    id: int
    name: str
    description: str

class QuizzEntity(Quizz):
    questions: Optional[list[Question]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class QuizzDto(QuizzEntity, BaseModel):
    id: int

class CreateQuizzDto(BaseModel):
    name: str
    description: str