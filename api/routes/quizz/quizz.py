from fastapi import APIRouter

router = APIRouter()

@router.get("/quizz")
async def get_quizz():
    return {"message": "get all available quizz"}

@router.get("/quizz/{quizz_id}")
async def get_quizz(quizz_id: int):
    return {"message": "get quizz"}

