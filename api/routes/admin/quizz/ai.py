from fastapi import APIRouter

admin_ai_router = APIRouter()

@admin_ai_router.post("/admin/quizz/ai")
async def post_ai_quizz():
    return {"message": "create a new quizz with AI"}

@admin_ai_router.get("/admin/quizz/ai")
async def get_ai_quizz():
    return {"message": "get all available quizz with AI"}

@admin_ai_router.get("/admin/quizz/ai/{quizz_id}")
async def get_ai_quizz(quizz_id: int):
    return {"message": "get quizz with AI"}

@admin_ai_router.delete("/admin/quizz/ai/{quizz_id}")
async def delete_ai_quizz(quizz_id: int):
    return {"message": "delete quizz with AI"}