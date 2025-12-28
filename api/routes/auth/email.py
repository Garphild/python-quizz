from fastapi import APIRouter

router = APIRouter()

@router.post("/auth/email")
async def post_email():
    return {"message": "auth via email"}
