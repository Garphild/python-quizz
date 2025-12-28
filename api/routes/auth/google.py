from fastapi import APIRouter

router = APIRouter()

@router.get("/auth/google")
async def get_google():
    return {"message": "get google auth url"}

@router.get("/auth/google/callback")
async def get_google_callback():
    return {"message": "get google auth callback"}