from fastapi import APIRouter, Path, Body, HTTPException
from routes.dto.question_dto import QuestionDto, CreateQuestionDto, UpdateQuestionDto
from typing import Annotated
from fastapi import Depends
from services.deps import get_questions_service
from services.question_service import QuestionsService

question_router = APIRouter(prefix="/api/quizz/{quizz_id}/questions", tags=["quizz -> questions"])

@question_router.get("/")
async def get_questions(
    quizz_id: Annotated[
        int, 
        Path(description="Quizz ID", examples=[1])
    ],
    question_service: QuestionsService = Depends(get_questions_service)
) -> list[QuestionDto]:
    return question_service.get_questions(quizz_id)

@question_router.get("/{question_id}")
async def get_question(
    quizz_id: Annotated[
        int, 
        Path(description="Quizz ID", examples=[1])
    ],
    question_id: Annotated[
        int, 
        Path(description="Question ID", examples=[1])
    ],
    question_service: QuestionsService = Depends(get_questions_service)
) -> QuestionDto:
    question = question_service.get_question_by_id(quizz_id, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question

@question_router.post("/")
async def create_question(
    quizz_id: Annotated[
        int, 
        Path(description="Quizz ID", examples=[1])
    ],
    question: Annotated[
        CreateQuestionDto, 
        Body(
            description="Question data", 
            examples=[{"text": "Question text"}]
        )
    ],
    question_service: QuestionsService = Depends(get_questions_service)
) -> QuestionDto:
    return question_service.create_question(quizz_id, question)

@question_router.put("/{question_id}")
async def update_question(
    quizz_id: Annotated[
        int, 
        Path(description="Quizz ID", examples=[1])
    ],
    question_id: Annotated[
        int, 
        Path(description="Question ID", examples=[1])
    ], 
    question: Annotated[
        UpdateQuestionDto, 
        Body(
            description="Question data", 
            examples=[{"text": "Question text"}]
        )
    ],
    question_service: QuestionsService = Depends(get_questions_service) 
) -> QuestionDto:
    currentQuestion = question_service.get_question_by_id(quizz_id, question_id)
    if not currentQuestion:
        raise HTTPException(status_code=404, detail="Question not found")

    createdQuestion = question_service.update_question(quizz_id, question_id, question)
    if not createdQuestion:
        raise HTTPException(status_code=404, detail="Question not found")

    return createdQuestion

@question_router.delete("/{question_id}")
async def delete_question(
    quizz_id: Annotated[
        int, 
        Path(description="Quizz ID", examples=[1])
    ],
    question_id: Annotated[
        int, 
        Path(description="Question ID", examples=[1])
    ],
    question_service: QuestionsService = Depends(get_questions_service)
) -> bool:
    currentQuestion = question_service.get_question_by_id(quizz_id, question_id)
    if not currentQuestion:
        raise HTTPException(status_code=404, detail="Question not found")

    question_service.delete_question(quizz_id, question_id)
    return True