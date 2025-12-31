from providers.models.user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Request

class UserRepository:
    db: AsyncSession | None = None
    
    def __init__(self, request: Request):
        self.db = request.state.db_sessionmaker()
    
    async def get_user_model_by_email(self, email: str) -> UserModel | None:
        stmt = select(UserModel).filter(UserModel.email == email, UserModel.deleted_at.is_(None))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_model_by_id(self, id: int) -> UserModel | None:
        stmt = select(UserModel).filter(UserModel.id == id, UserModel.deleted_at.is_(None))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def add(self, email: str, name: str, surname: str, password: str) -> UserModel:
        user_model = UserModel()
        user_model.email = email
        user_model.name = name
        user_model.surname = surname
        user_model.password = password

        self.db.add(user_model)
        return user_model
    
    async def delete(self, id: int) -> bool:
        user_model = await self.get_user_model_by_id(id)
        if user_model is None:
            return False

        user_model.soft_delete()
        await self.db.merge(user_model)
        return True

    
    async def update(
        self,
        id: int,
        email: str | None = None,
        name: str | None = None,
        surname: str | None = None,
        password: str | None = None,
    ) -> UserModel | None:
        user_model = await self.get_user_model_by_id(id)

        if user_model is None:
            return None

        if password is not None:
            user_model.password = password

        if email is not None:
            user_model.email = email
        
        if name is not None:
            user_model.name = name
        
        if surname is not None:
            user_model.surname = surname
        
        await self.db.merge(user_model)
        return user_model
