from fastapi import Request
from repositories.user_repository import UserRepository

def get_user_repository(request: Request):
    return UserRepository(request.state.db_sessionmaker())