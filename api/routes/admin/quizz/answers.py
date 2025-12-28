from fastapi import APIRouter

admin_answers_router = APIRouter()

@admin_answers_router.get("/admin/quizz/{quizz_id}/answers")
async def get_answers(quizz_id: int):
    return {"message": "get all available answers"}

@admin_answers_router.post("/admin/quizz/{quizz_id}/answers")
async def post_answers(quizz_id: int):
    return {"message": "create a new answer"}

@admin_answers_router.put("/admin/quizz/{quizz_id}/answers/{answer_id}")
async def put_answers(quizz_id: int, answer_id: int):
    return {"message": "update answer"}

@admin_answers_router.delete("/admin/quizz/{quizz_id}/answers/{answer_id}")
async def delete_answers(quizz_id: int, answer_id: int):
    return {"message": "delete answer"}