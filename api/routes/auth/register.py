from fastapi import APIRouter

router = APIRouter()

@router.post("/auth/register")
async def post_register():
    return {"message": "register"}