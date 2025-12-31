from providers.models.user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Request

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_model_by_email(self, email: str):
        stmt = select(UserModel).filter(UserModel.email == email, UserModel.deleted_at.is_(None))

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

def get_user_repository(request: Request):
    return UserRepository(request.state.db_sessionmaker())