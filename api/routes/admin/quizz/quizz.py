from fastapi import APIRouter
from entities.quizz import CreateQuizzDto, QuizzDto

admin_quizz_router = APIRouter()

@admin_quizz_router.get("/admin/quizz?page={page}&limit={limit}")
async def get_quizz(page: int = 0, limit: int = 10) -> list[QuizzDto]:
    return []

@admin_quizz_router.post("/admin/quizz")
async def post_quizz(quizz: CreateQuizzDto) -> QuizzDto:
    return QuizzDto()

@admin_quizz_router.put("/admin/quizz/{quizz_id}")
async def put_quizz(quizz_id: int) -> QuizzDto:
    return QuizzDto()

@admin_quizz_router.delete("/admin/quizz/{quizz_id}")
async def delete_quizz(quizz_id: int) -> QuizzDto:
    return QuizzDto()

@admin_quizz_router.get("/admin/quizz/{quizz_id}")
async def get_quizz(quizz_id: int) -> QuizzDto:
    return QuizzDto()