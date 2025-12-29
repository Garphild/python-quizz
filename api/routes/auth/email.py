from fastapi import APIRouter
from authx import AuthX, AuthXConfig
from fastapi import Body, HTTPException
from typing import Annotated

from routes.auth.dto.auth_dto import LoginRequest
from services.user_service import UserService

config = AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY="your-secret-key-here",
    JWT_ACCESS_COOKIE_NAME="auth_token",
    JWT_TOKEN_LOCATION=["cookies"]
)

security = AuthX(config=config)

email_auth_router = APIRouter(prefix="/api/auth", tags=["auth"])




