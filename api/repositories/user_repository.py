from providers.models.user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Request

class UserRepository:
    db: AsyncSession | None = None
    
    def __init__(self, request: Request):
        self.db = request.state.db_sessionmaker()
    
    async def get_user_model_by_email(self, email: str) -> UserModel:
        try:
            stmt = select(UserModel).filter(UserModel.email == email, UserModel.deleted_at.is_(None))
            result = await self.db.execute(stmt)
        except Exception as e:
            print(e)
            raise Exception("Failed to get user")
        else:
            return result.scalar_one_or_none()

    async def get_user_model_by_id(self, id: int) -> UserModel:
        try:
            stmt = select(UserModel).filter(UserModel.id == id, UserModel.deleted_at.is_(None))
            result = await self.db.execute(stmt)
        except Exception as e:
            print(e)
            raise Exception("Failed to get user")
        else:
            return result.scalar_one_or_none()
    
    async def add(self, email: str, name: str, surname: str, password: str, auto_commit: bool = True) -> UserModel:
        try:
            user_model = UserModel()
            user_model.email = email
            user_model.name = name
            user_model.surname = surname
            user_model.password = password

            self.db.add(user_model)
        except Exception as e:
            print(e)
            if auto_commit:
                await self.db.rollback()
            raise Exception("Failed to add user")
        else:
            if auto_commit:
                await self.db.commit()
            await self.db.refresh(user_model)
            return user_model
    
    async def delete(self, id: int, auto_commit: bool = True) -> bool:
        try:
            user_model = await self.get_user_model_by_id(id)
            if user_model is None:
                raise Exception("User not found")

            user_model.soft_delete()

            await self.db.merge(user_model)
        except Exception as e:
            print(e)
            if auto_commit:
                await self.db.rollback()
            raise Exception("Failed to delete user")
        else:
            if auto_commit:
                await self.db.commit()
            return True

    
    async def update(
        self,
        id: int,
        email: str | None = None,
        name: str | None = None,
        surname: str | None = None,
        password: str | None = None,
        auto_commit: bool = True
    ) -> UserModel:
        try:               
            user_model = await self.get_user_model_by_id(id)
            
            if user_model is None:
                raise Exception("User not found")
            
            if password is not None:
                user_model.password = password

            if email is not None:
                user_model.email = email
            
            if name is not None:
                user_model.name = name
            
            if surname is not None:
                user_model.surname = surname
            
            await self.db.merge(user_model)
        except Exception as e:
            print(e)
            if auto_commit:
                await self.db.rollback()
            raise Exception("Failed to update user")
        else:
            if auto_commit:
                await self.db.commit()
            await self.refresh(user_model)
            return user_model

    async def rollback(self):
        await self.db.rollback()

    async def commit(self):
        await self.db.commit()
    
    async def refresh(self, user_model: UserModel):
        await self.db.refresh(user_model)
