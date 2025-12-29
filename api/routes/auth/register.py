from entities.user import PublicUser
from fastapi import APIRouter, Body, HTTPException
from typing import Annotated
from routes.auth.dto.auth_dto import RegisterRequest
from services.user_service import UserService

