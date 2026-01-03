from fastapi import APIRouter, Body, HTTPException, Response, Request
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

    if existing_user is not None:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    user = await user_service.create_user(
        password=newUser.password,
        email=newUser.email,
        name=newUser.name,
        surname=newUser.surname
    )

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
    user = await user_service.get_user_model_by_email(loginReq.email)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.verify_password(loginReq.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = security.create_access_token(uid=str(user.id))
    refresh_token = security.create_refresh_token(uid=str(user.id))

    security.set_access_cookies(access_token, response=response)
    security.set_refresh_cookies(refresh_token, response=response)
    
    return ProfileDto.from_orm(user)

@authRouter.post("/logout")
async def logout(
    response: Response,
    user_service: UserService = Depends(get_user_service)
) -> bool:
    security.unset_cookies(response)
    return True


@authRouter.post("/refresh")
async def refresh_tokens(
    request: Request,
    response: Response,
) -> dict[str, str]:
    try:
        refresh_payload = await security.refresh_token_required(request)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    uid = str(refresh_payload.sub)
    new_access_token = security.create_access_token(uid=uid)
    new_refresh_token = security.create_refresh_token(uid=uid)

    security.set_access_cookies(new_access_token, response=response)
    security.set_refresh_cookies(new_refresh_token, response=response)

    return {"access_token": new_access_token}

@authRouter.get("/profile")
async def get_profile(
    user_service: UserService = Depends(get_user_service),
    user_id: int = Depends(security.get_current_subject)
) -> ProfileDto:
    user_model = await user_service.get_user_model_by_id(user_id)
    
    if not user_model:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return ProfileDto.from_orm(user_model)

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

    return ProfileDto.from_orm(user_model)

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

    return ProfileDto.from_orm(user_model)
