from pydantic import BaseModel
from typing import Optional, Annotated
from pydantic import Field

class AnswerDto(BaseModel):
    id: Annotated[int, Field(description="Answer ID", example=1)]
    text: Annotated[str, Field(description="Answer text", example="Answer text")]
    is_correct: Annotated[bool, Field(description="Is correct", example=True)]
    question_id: Annotated[int, Field(description="Linked Question Id")]
    description: Annotated[str, Field(description="Description", example="Description")]
    valid_description: Optional[Annotated[str, Field(description="Valid description", example="Valid description")]]

class CreateAnswerDto(BaseModel):
    text: Annotated[str, Field(description="Answer text", example="Answer text")]
    is_correct: Annotated[bool, Field(description="Is correct", example=True)]
    description: Annotated[str, Field(description="Description", example="Description")]
    valid_description: Optional[Annotated[str, Field(description="Valid description", example="Valid description")]]

class UpdateAnswerDto(BaseModel):
    text: Annotated[str, Field(description="Answer text", example="Answer text")]
    is_correct: Annotated[bool, Field(description="Is correct", example=True)]
    description: Annotated[str, Field(description="Description", example="Description")]
    valid_description: Optional[Annotated[str, Field(description="Valid description", example="Valid description")]]

class ValidateAnswerDto(BaseModel):
    is_correct: Annotated[bool, Field(description="Is correct", example=True)]
    description: Annotated[str, Field(description="Description", example="Description")]
    valid_description: Optional[Annotated[str, Field(description="Valid description", example="Valid description")]]