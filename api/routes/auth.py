from fastapi import APIRouter, Body, HTTPException
from typing import Annotated
from routes.dto.auth_dto import ChangePasswordDto, RegisterRequestDto, ProfileDto, LoginRequestDto, UpdateProfileDto
from services.user_service import user_service
from authx import AuthX, AuthXConfig

config = AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY="your-secret-key-here",
    JWT_ACCESS_COOKIE_NAME="auth_token",
    JWT_TOKEN_LOCATION=["cookies"]
)

security = AuthX(config=config)

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
    ]
) -> bool | None:
    existing_user = await user_service.get_by_email(newUser.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    user = await user_service.create_user(newUser)

    return True

@authRouter.post("/login")
async def login(
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
    ]
) -> ProfileDto:
    user = await user_service.get_by_email(loginReq.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.verify_password(loginReq.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = security.create_access_token(uid=str(user.id))
    
    # Return a success response (token generation would go here)
    return ProfileDto.validate_model(user)

@authRouter.post("/logout")
async def logout() -> bool:
    security.logout()

    return True

@authRouter.get("/profile")
async def get_profile() -> ProfileDto:
    user_id = security.get_current_user_id()

    user = await user_service.get_by_id(user_id)

    return ProfileDto.validate_model(user)

@authRouter.post("/change-password")
async def change_password(
    data: ChangePasswordDto
) -> ProfileDto:
    user_id = security.get_current_user_id()

    user = await user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.verify_password(data.old_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    await user_service.update_password(user_id, data.new_password)

    return ProfileDto.validate_model(user)

@authRouter.post("/update-profile")
async def update_profile(
    data: UpdateProfileDto
) -> ProfileDto:
    user_id = security.get_current_user_id()

    user = await user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    await user_service.update_profile(user_id, data)

    return ProfileDto.validate_model(user)
