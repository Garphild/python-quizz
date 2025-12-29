from fastapi import APIRouter, Path, Body
from routes.dto.quizz_dto import QuizzDto, CreateQuizzDto, UpdateQuizzDto
from typing import Annotated

from services.quizz_service import quizzService

quizz_router = APIRouter(prefix="/api/quizz", tags=["quizz"])

@quizz_router.get("/", description="Get all available quizz")
async def get_quizz() -> list[QuizzDto]:
    return quizzService.get_all()

@quizz_router.get("/{quizz_id}", description="Get quizz by id")
async def get_quizz(quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])]) -> QuizzDto:
    return quizzService.get_by_id(quizz_id)

@quizz_router.post("/", description="Create new quizz")
async def create_quizz(
    quizz: Annotated[
        CreateQuizzDto,
        Body(description="Quizz data", examples=[{"url": "https://www.youtube.com/watch?v=example"}])
    ]
) -> QuizzDto:
    return quizzService.create(quizz)

@quizz_router.put("/{quizz_id}", description="Update quizz by id")
async def update_quizz(
    quizz_id: Annotated[
        int, 
        Path(description="Quizz ID", examples=[1])
    ],
    quizz: Annotated[
        UpdateQuizzDto,
        Body(description="Quizz data", examples=[{"name": "Quizz name", "description": "Quizz description"}])
    ]
) -> QuizzDto:
    return quizzService.update(quizz_id, quizz)

@quizz_router.delete("/{quizz_id}", description="Delete quizz by id")
async def delete_quizz(
    quizz_id: Annotated[
        int,
        Path(description="Quizz ID", examples=[1])
    ]
) -> bool:
    return quizzService.delete(quizz_id)
