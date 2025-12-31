from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field

class PublicAnswer(BaseModel):
    id: Annotated[int, Field(gt=0, description="Answer ID")]
    answer: Annotated[str, Field(min_length=1, max_length=1000, description="Answer text")]
    quiz_id: Annotated[int, Field(gt=0, description="Quiz ID")]
    description: Annotated[Optional[str], Field(max_length=1000, description="Answer description")] = None
    created_at: Annotated[Optional[datetime], Field(description="Creation timestamp")] = None
    updated_at: Annotated[Optional[datetime], Field(description="Last update timestamp")] = None
    deleted_at: Annotated[Optional[datetime], Field(description="Deletion timestamp")] = None

class AnswerEntity(PublicAnswer, BaseModel):
    is_correct: Annotated[bool, Field(description="Whether this answer is correct")]

    class Config:
        from_attributes = True
