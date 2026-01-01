from fastapi import APIRouter, Body, HTTPException, Response
from typing import Annotated
from routes.dto.auth_dto import ChangePasswordDto, RegisterRequestDto, ProfileDto, LoginRequestDto, UpdateProfileDto
from fastapi import Depends
from services.user_service import UserService
from services.deps import get_user_service
from core.security import security

authRouter = APIRouter(prefix="/api/auth", tags=["auth"])

@authRouter.post("/register")
async def post_register(
    newUser: Annotated[
        RegisterRequestDto,
        Body(
            description="Register request",
            examples=[
                {
                    "email": "user@example.com",
                    "password": "password123",
                    "name": "John",
                    "surname": "Doe"
                }
            ]
        )
    ],
    user_service: UserService = Depends(get_user_service)
) -> bool | None:
    existing_user = await user_service.get_user_model_by_email(newUser.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    user = await user_service.create_user(newUser)

    if not user:
        raise HTTPException(status_code=500, detail="Failed to create user")

    return True

@authRouter.post("/login")
async def login(
    response: Response,
    loginReq: Annotated[
        LoginRequestDto, 
        Body(
            description="Login request", 
            examples={
                "example1": {
                    "summary": "Example login", 
                    "value": {
                        "email": "user@example.com", 
                        "password": "password123"
                    }
                }
            }
        )
    ],
    user_service: UserService = Depends(get_user_service)
) -> ProfileDto:
    profile = await user_service.verify_login(loginReq.email, loginReq.password)
    if not profile:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = security.create_access_token(uid=str(profile.id))
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        max_age=3600 * 24,
        samesite="lax"
    )
    
    return profile

@authRouter.post("/logout")
async def logout(
    user_service: UserService = Depends(get_user_service)
) -> bool:
    security.logout()

    return True

@authRouter.get("/profile")
async def get_profile(
    user_service: UserService = Depends(get_user_service),
    user_id: int = Depends(security.get_current_subject)
) -> ProfileDto:
    user_model = await user_service.get_user_model_by_id(user_id)

    return ProfileDto.model_validate(user_model)

@authRouter.post("/change-password")
async def change_password(
    data: ChangePasswordDto,
    user_service: UserService = Depends(get_user_service),
    user_id: int = Depends(security.get_current_subject)
) -> ProfileDto:
    user_model = await user_service.get_user_model_by_id(user_id)

    if not user_model:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user_model.verify_password(data.old_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    await user_service.update_password(user_id, data.new_password)

    return ProfileDto.model_validate(user_model)

@authRouter.post("/update-profile")
async def update_profile(
    data: UpdateProfileDto,
    user_service: UserService = Depends(get_user_service),
    user_id: int = Depends(security.get_current_subject)
) -> ProfileDto:
    user_model = await user_service.get_user_model_by_id(user_id)

    if not user_model:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    await user_service.update_profile(user_id, data)

    return ProfileDto.model_validate(user_model)
