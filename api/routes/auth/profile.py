from fastapi import APIRouter

profile_router = APIRouter()

@profile_router.get("/auth/profile")
async def get_profile():
    return {"message": "get profile"}

@profile_router.put("/auth/profile")
async def update_profile():
    return {"message": "update profile"}

@profile_router.delete("/auth/profile")
async def delete_profile():
    return {"message": "delete profile"}

@profile_router.get("/auth/logout")
async def logout():
    return {"message": "logout"}