from fastapi import APIRouter, Path
from routes.dto.answer_dto import CreateAnswerDto, UpdateAnswerDto, AnswerDto, ValidateAnswerDto
from services.answer_service import answerService
from typing import Annotated

answer_router = APIRouter(prefix="/api/quizz/{quizz_id}/questions/{question_id}/answers", tags=["quizz -> question -> answers"])

@answer_router.get("/")
async def get_answers(quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])], question_id: Annotated[int, Path(description="Question ID", examples=[1])]) -> list[AnswerDto]:
    quizz_answers = answerService.get_answers(quizz_id)
    return [AnswerDto(**answer) for answer in quizz_answers]

@answer_router.get("/{answer_id}")
async def get_answer(quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])], answer_id: Annotated[int, Path(description="Answer ID", examples=[1])]) -> AnswerDto:
    answer = answerService.get_answer(quizz_id, answer_id)
    return AnswerDto(**answer)

@answer_router.post("/")
async def create_answer(quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])], answer: CreateAnswerDto) -> AnswerDto:
    created_answer = answerService.create_answer(quizz_id, answer)
    return AnswerDto(**created_answer)

@answer_router.put("/{answer_id}")
async def update_answer(quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])], answer_id: Annotated[int, Path(description="Answer ID", examples=[1])], answer: UpdateAnswerDto) -> AnswerDto:
    updated_answer = answerService.update_answer(quizz_id, answer_id, answer)
    return AnswerDto(**updated_answer)

@answer_router.delete("/{answer_id}")
async def delete_answer(quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])], answer_id: Annotated[int, Path(description="Answer ID", examples=[1])]) -> bool:
    answerService.delete_answer(quizz_id, answer_id)

    return True

@answer_router.get("/validate/{answer_id}")
async def validate_answer(
    quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])], 
    question_id: Annotated[int, Path(description="Question ID", examples=[1])],
    answer_id: Annotated[int, Path(description="Answer ID", examples=[1])]
) -> ValidateAnswerDto:
    validation_result = answerService.validate_answer(quizz_id, question_id, answer_id)
    return ValidateAnswerDto(**validation_result)