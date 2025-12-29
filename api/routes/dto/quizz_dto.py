from typing import Optional, Annotated
from datetime import datetime
from pydantic import BaseModel, Field

class QuizzDto(BaseModel):
    id: Annotated[int, Field(description="Quizz ID", example=1)]
    name: Annotated[str, Field(description="Quizz name", example="Quizz name")]
    description: Annotated[str, Field(description="Quizz description", example="Quizz description")]
    url: Annotated[str, Field(description="Quizz URL", example="quizz_url")]
    questions_count: Annotated[int, Field(description="Quizz questions count", example=10)]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class CreateQuizzDto(BaseModel):
    url: Annotated[str, Field(description="Youtube URL", example="https://www.youtube.com/watch?v=example")]

class UpdateQuizzDto(BaseModel):
    name: Annotated[str, Field(description="Quizz name", example="Quizz name")] = None
    description: Annotated[str, Field(description="Quizz description", example="Quizz description")] = None