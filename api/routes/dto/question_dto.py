from datetime import datetime
from typing import Annotated
from pydantic import Field, BaseModel

class QuestionDto(BaseModel):
    id: Annotated[int, Field(description="Question ID")]
    text: Annotated[str, Field(description="Question text")]
    created_at: Annotated[datetime, Field(description="Creation timestamp")]
    updated_at: Annotated[datetime, Field(description="Update timestamp")]
    deleted_at: Annotated[datetime | None, Field(description="Deletion timestamp", default=None)]

class CreateQuestionDto(BaseModel):
    text: Annotated[str, Field(description="Question text")]

class UpdateQuestionDto(BaseModel):
    text: Annotated[str, Field(description="Question text")]

class QuestionListDto(BaseModel):
    questions: Annotated[list[QuestionDto], Field(description="List of questions")]