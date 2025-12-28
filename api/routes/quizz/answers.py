from fastapi import APIRouter

router = APIRouter()

@router.get("/quizz/{quizz_id}/answers")
async def get_answers(quizz_id: int):
    return {"message": "get all available answers"}

@router.get("/quizz/{quizz_id}/answers/{answer_id}")
async def get_answer(quizz_id: int, answer_id: int):
    return {"message": "get answer"}