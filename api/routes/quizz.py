from fastapi import APIRouter, Path, Body
from routes.dto.quizz_dto import QuizzDto, CreateQuizzDto, UpdateQuizzDto
from typing import Annotated
from fastapi import HTTPException
from fastapi import Depends
from services.deps import get_quizz_service
from services.quizz_service import QuizzService
from core.security import security

quizz_router = APIRouter(prefix="/api/quizz", tags=["quizz"])

@quizz_router.get("/", description="Get all available quizz")
async def get_all_quizzes(
    user_id: int = Depends(security.get_current_subject),
    quizz_service: QuizzService = Depends(get_quizz_service)
) -> list[QuizzDto]:
    return await quizz_service.get_all(user_id)

@quizz_router.get("/{quizz_id}", description="Get quizz by id")
async def get_quizz_by_id(
    quizz_id: Annotated[int, Path(description="Quizz ID", examples=[1])],
    user_id: int = Depends(security.get_current_subject),
    quizz_service: QuizzService = Depends(get_quizz_service)
) -> QuizzDto:
    quizz = await quizz_service.get_by_id(quizz_id, user_id)
    if not quizz:
        raise HTTPException(status_code=404, detail="Quizz not found")

    return QuizzDto.from_orm(quizz)

@quizz_router.post("/", description="Create new quizz")
async def create_quizz(
    quizz: Annotated[
        CreateQuizzDto,
        Body(description="Quizz data", examples=[{"url": "https://www.youtube.com/watch?v=example"}])
    ],
    user_id: int = Depends(security.get_current_subject),
    quizz_service: QuizzService = Depends(get_quizz_service)
) -> QuizzDto:
    quizz = await quizz_service.create(quizz.url)
    if not quizz:
        raise HTTPException(status_code=404, detail="Quizz not found")

    return QuizzDto.from_orm(quizz)

@quizz_router.put("/{quizz_id}", description="Update quizz by id")
async def update_quizz(
    quizz_id: Annotated[
        int, 
        Path(description="Quizz ID", examples=[1])
    ],
    quizz: Annotated[
        UpdateQuizzDto,
        Body(description="Quizz data", examples=[{"name": "Quizz name", "description": "Quizz description"}])
    ],
    user_id: int = Depends(security.get_current_subject),
    quizz_service: QuizzService = Depends(get_quizz_service)
) -> QuizzDto:
    quizz = await quizz_service.update(quizz_id, quizz, user_id)
    if not quizz:
        raise HTTPException(status_code=404, detail="Quizz not found")

    return QuizzDto.from_orm(quizz)

@quizz_router.delete("/{quizz_id}", description="Delete quizz by id")
async def delete_quizz(
    quizz_id: Annotated[
        int,
        Path(description="Quizz ID", examples=[1])
    ],
    user_id: int = Depends(security.get_current_subject),
    quizz_service: QuizzService = Depends(get_quizz_service)
) -> bool:
    quizz = await quizz_service.delete(quizz_id, user_id)
    if not quizz:
        raise HTTPException(status_code=404, detail="Quizz not found")

    return True
