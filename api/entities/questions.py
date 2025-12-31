from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field

class Question(BaseModel):
    id: Annotated[int, Field(gt=0, description="Question ID")]
    question: Annotated[str, Field(min_length=1, max_length=1000, description="Question text")]
    
class QuestionEntity(Question, BaseModel):
    created_at: Annotated[Optional[datetime], Field(description="Creation timestamp")] = None
    updated_at: Annotated[Optional[datetime], Field(description="Last update timestamp")] = None
    deleted_at: Annotated[Optional[datetime], Field(description="Deletion timestamp")] = None

    class Config:
        from_attributes = True

