from fastapi import Request
from sqlalchemy import select
from providers.models.quizz_model import QuizzModel
from sqlalchemy.ext.asyncio import AsyncSession
from errors.item_not_found import ItemNotFound
from errors.database_error import DatabaseError

class QuizzRepository:
    db: AsyncSession | None = None
    
    def __init__(self, db: AsyncSession):
        self.db = db

        if self.db is None:
            raise DatabaseError("Database session is not initialized")

    '''
    Get quizz model by id
    @param id: int
    @param user_id: int
    @return: QuizzModel
    @throws: ItemNotFound
    @throws: DatabaseError
    '''
    async def get_quizz_model_by_id(
        self,
        id: int,
        user_id: int
    ) -> QuizzModel:
        try:
            stmt = select(QuizzModel).filter(
                QuizzModel.id == id,
                QuizzModel.deleted_at.is_(None),
                QuizzModel.user_id == user_id
            )
            result = await self.db.execute(stmt)
            result = result.scalar_one_or_none()
        except Exception:
            raise DatabaseError("Failed to get quizz model by id")

        if result is None:
            raise ItemNotFound("Quizz not found")
        
        return result

    '''
    Get all quizz models
    @param user_id: int
    @return: list[QuizzModel]
    @throws: ItemNotFound
    @throws: DatabaseError
    '''
    async def get_all_quizz_models(
        self,
        user_id: int
    ) -> list[QuizzModel]:
        try:
            stmt = select(QuizzModel).filter(
                QuizzModel.deleted_at.is_(None),
                QuizzModel.user_id == user_id
            )
            result = await self.db.execute(stmt)
            result = result.scalars().all()
        except Exception:
            raise DatabaseError("Failed to get all quizz models")
        
        if result is None:
            raise ItemNotFound("Quizzes not found")
        
        return result

    '''
    Create new quizz
    @param name: str
    @param description: str
    @param user_id: int
    @param url: str
    @return: QuizzModel
    @throws: DatabaseError
    '''
    async def add(
        self,
        name: str,
        description: str,
        user_id: int,
        url: str
    ) -> QuizzModel:
        try:
            quizz_model = QuizzModel()
            quizz_model.name = name
            quizz_model.description = description
            quizz_model.user_id = user_id
            quizz_model.url = url
            await self.db.add(quizz_model)
            await self.db.refresh(quizz_model)
        except Exception:
            raise DatabaseError("Failed to add quizz")
        
        return quizz_model

    '''
    Update existing quizz
    @param id: int
    @param name: str | None
    @param description: str | None
    @param user_id: int | None
    @return: QuizzModel | None
    @throws: ItemNotFound
    @throws: DatabaseError
    '''    
    async def update(
        self,
        id: int,
        name: str | None = None,
        description: str | None = None,
        user_id: int | None = None,
    ) -> QuizzModel | None:
        try:
            quizz_model = await self.get_quizz_model_by_id(
                id,
                user_id
            )
        except Exception:
            raise DatabaseError("Failed to get quizz model")
        
        if quizz_model is None:
            raise ItemNotFound("Quizz not found")
        
        quizz_model.name = name or quizz_model.name
        quizz_model.description = description or quizz_model.description
        quizz_model.user_id = user_id or quizz_model.user_id
        try:
            await self.db.merge(quizz_model)
            await self.db.refresh(quizz_model)
        except Exception:
            raise DatabaseError("Failed to update quizz")
        
        return quizz_model

    '''
    Delete quizz
    @param id: int
    @param user_id: int
    @return: bool
    @throws: ItemNotFound
    @throws: DatabaseError
    '''
    async def delete(self, id: int, user_id: int) -> bool:
        try:
            quizz_model = await self.get_quizz_model_by_id(
                id,
                user_id
            )
        except Exception:
            raise DatabaseError("Failed to delete quizz")

        if quizz_model is None:
            raise ItemNotFound("Quizz not found")
        
        quizz_model.soft_delete()
        try:
            await self.db.merge(quizz_model)
        except Exception:
            raise DatabaseError("Failed to delete quizz")
        
        return True
