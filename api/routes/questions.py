from fastapi import APIRouter, Query, Path, Body, HTTPException
from routes.dto.question_dto import QuestionDto, CreateQuestionDto, UpdateQuestionDto
from services.question_service import questionService
from typing import Annotated

question_router = APIRouter(prefix="/api/quizz/{quizz_id}/questions", tags=["quizz -> questions"])

@question_router.get("/")
async def get_questions(quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])]):
    return questionService.get_all_by_quizz_id(quizz_id)

@question_router.get("/{question_id}")
async def get_question(
    quizz_id: Annotated[
        int, 
        Path(description="Quizz ID", examples=[1])
    ],
    question_id: Annotated[
        int, 
        Path(description="Question ID", examples=[1])
    ]
) -> QuestionDto:
    currentQuestion = questionService.get_by_id(quizz_id, question_id)
    if not currentQuestion:
        raise HTTPException(status_code=404, detail="Question not found")

    return currentQuestion

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
    ]
) -> QuestionDto:
    return questionService.create(quizz_id, question)

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
    ]
) -> QuestionDto:
    currentQuestion = questionService.get_by_id(quizz_id, question_id)
    if not currentQuestion:
        raise HTTPException(status_code=404, detail="Question not found")

    createdQuestion = questionService.update(quizz_id, question_id, question)
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
    ]
) -> bool:
    currentQuestion = questionService.get_by_id(quizz_id, question_id)
    if not currentQuestion:
        raise HTTPException(status_code=404, detail="Question not found")

    questionService.delete(quizz_id, question_id)
    return True