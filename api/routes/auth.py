from fastapi import APIRouter, Body, HTTPException
from typing import Annotated
from routes.auth.dto.auth_dto import RegisterRequestDto, ProfileDto, LoginRequestDto
from services.user_service import UserService
from core.security import security

authRouter = APIRouter(prefix="/api/auth", tags=["auth"])

@authRouter.post("/register")
async def post_register(newUser: Annotated[RegisterRequestDto, Body(description="Register request")]) -> ProfileDto | None:
    userService = UserService()

    existing_user = await userService.get_by_email(newUser.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    user = await userService.create_user(newUser)

    return ProfileDto(
        id=str(user.id), 
        email=user.email, 
        name=user.name, 
        surname=user.surname, 
        created_at=user.created_at.isoformat() if user.created_at else None
    )

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
    user_service = UserService()
    user = await user_service.get_by_email(loginReq.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.verify_password(loginReq.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = security.create_access_token(uid=str(user.id))
    
    # Return a success response (token generation would go here)
    return ProfileDto(
        id=str(user.id), 
        email=user.email, 
        name=user.name, 
        surname=user.surname, 
        created_at=user.created_at.isoformat() if user.created_at else None
    )