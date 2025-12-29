from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field

class PublicAnswer:
    id: int
    answer: str
    quiz_id: int

class Answer(PublicAnswer):
    is_correct: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class AnswerEntity(Answer):
    pass

class PublicAnswerDto(BaseModel):
    id: Annotated[int, Field(description="Answer ID")]
    answer: Annotated[str, Field(description="Answer text")]
    quiz_id: Annotated[int, Field(description="Quiz ID")]

class AnswerDto(PublicAnswerDto):
    is_correct: Annotated[bool, Field(description="Whether this answer is correct")]

class CreateAnswerDto(BaseModel):
    answer: Annotated[str, Field(description="Answer text")]
    is_correct: Annotated[bool, Field(description="Whether this answer is correct")]

class UpdateAnswerDto(BaseModel):
    answer: Annotated[Optional[str], Field(description="Answer text")]
    is_correct: Annotated[Optional[bool], Field(description="Whether this answer is correct")]