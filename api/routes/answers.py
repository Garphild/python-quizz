from fastapi import APIRouter, Path, HTTPException, Depends
from routes.dto.answer_dto import CreateAnswerDto, UpdateAnswerDto, AnswerDto, ValidateAnswerDto
from typing import Annotated
from services.answer_service import AnswerService
from services.quizz_service import QuizzService
from services.deps import get_answer_service, get_quizz_service
from core.security import security
from logging import getLogger
from errors.item_not_found import ItemNotFound

logger = getLogger(__name__)

answer_router = APIRouter(prefix="/api/quizz/{quizz_id}/questions/{question_id}/answers", tags=["quizz -> question -> answers"])

@answer_router.get("/")
async def get_answers(
    quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])], 
    question_id: Annotated[int, Path(description="Question ID", examples=[1])],
    answer_service: AnswerService = Depends(get_answer_service),
    quizz_service: QuizzService = Depends(get_quizz_service),
    user_id: int = Depends(security.get_current_subject)
) -> list[AnswerDto]:
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")


    try:
        quizz = await quizz_service.get_by_id(quizz_id, user_id)
        answers = await answer_service.get_answers_by_question_id(question_id)
    except ItemNotFound as e:
        raise HTTPException(status_code=404, detail="Quizz answers not found")
    except Exception as e:
        logger.error(f"Error getting quizz answers: {e}")
        raise HTTPException(status_code=500, detail="Internal error")


    

    return [AnswerDto.from_orm(answer) for answer in answers]

@answer_router.get("/{answer_id}")
async def get_answer(
    quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])], 
    question_id: Annotated[int, Path(description="Question ID", examples=[1])], 
    answer_id: Annotated[int, Path(description="Answer ID", examples=[1])], 
    answer_service: AnswerService = Depends(get_answer_service)
) -> AnswerDto:
    answer = answer_service.get_answer_by_id(answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    return AnswerDto.from_orm(answer)

@answer_router.post("/")
async def create_answer(
    quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])], 
    question_id: Annotated[int, Path(description="Question ID", examples=[1])], 
    answer: CreateAnswerDto,
    answer_service: AnswerService = Depends(get_answer_service)
) -> AnswerDto:
    created_answer = answer_service.create_answer(quizz_id, question_id, answer)
    if not created_answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    return AnswerDto.from_orm(created_answer)

@answer_router.put("/{answer_id}")
async def update_answer(
    quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])],
    question_id: Annotated[int, Path(description="Question ID", examples=[1])],
    answer_id: Annotated[int, Path(description="Answer ID", examples=[1])],
    answer: UpdateAnswerDto,
    answer_service: AnswerService = Depends(get_answer_service)
) -> AnswerDto:
    updated_answer = answer_service.update_answer(quizz_id, question_id, answer_id, answer)
    if not updated_answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    return AnswerDto.from_orm(updated_answer)

@answer_router.delete("/{answer_id}")
async def delete_answer(
    quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])], 
    question_id: Annotated[int, Path(description="Question ID", examples=[1])], 
    answer_id: Annotated[int, Path(description="Answer ID", examples=[1])], 
    answer_service: AnswerService = Depends(get_answer_service)
) -> bool:
    answer_service.delete_answer(quizz_id, question_id, answer_id)
    return True

@answer_router.get("/validate/{answer_id}")
async def validate_answer(
    quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])], 
    question_id: Annotated[int, Path(description="Question ID", examples=[1])],
    answer_id: Annotated[int, Path(description="Answer ID", examples=[1])],
    answer_service: AnswerService = Depends(get_answer_service)
) -> ValidateAnswerDto:
    validation_result = answer_service.validate_answer(quizz_id, question_id, answer_id)
    if not validation_result:
        raise HTTPException(status_code=404, detail="Answer not found")

    return ValidateAnswerDto.from_orm(validation_result)