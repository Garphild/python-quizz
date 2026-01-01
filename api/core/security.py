from authx import AuthXConfig, AuthX
from core.settings import settings

authx_config: AuthXConfig = AuthXConfig(
    JWT_ALGORITHM=settings.JWT_ALGORITHM or "HS256",
    JWT_SECRET_KEY=settings.JWT_SECRET_KEY or "your-secret-key-here",
    JWT_ACCESS_COOKIE_NAME=settings.JWT_ACCESS_COOKIE_NAME or "auth_token",
    JWT_TOKEN_LOCATION=settings.JWT_TOKEN_LOCATION or ["cookies"]
)
security = AuthX(config=authx_config)   