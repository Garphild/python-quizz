from typing import Optional, Annotated
from datetime import datetime
from pydantic import BaseModel, Field

class Quizz(BaseModel):
    id: Annotated[int, Field(gt=0, description="Quizz ID")]
    name: Annotated[str, Field(min_length=1, max_length=100, description="Quizz name")]
    description: Annotated[str, Field(max_length=1000, description="Quizz description")]
    created_at: Annotated[Optional[datetime], Field(description="Creation timestamp")] = None
    updated_at: Annotated[Optional[datetime], Field(description="Last update timestamp")] = None
    deleted_at: Annotated[Optional[datetime], Field(description="Deletion timestamp")] = None

    class Config:
        from_attributes = True


