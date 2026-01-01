import logging
from sqlalchemy import select
from providers.models.quizz_model import QuizzModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from errors.item_not_found import ItemNotFound
from errors.database_error import DatabaseError

logger = logging.getLogger(__name__)

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
            quizz_model = result.scalar_one_or_none()
        except SQLAlchemyError as exc:
            logger.exception("Failed to get quizz model by id: %s", id)
            raise DatabaseError("Failed to get quizz model by id") from exc
        except Exception as e:
            logger.exception("Failed to get quizz model by id: %s", id)
            raise DatabaseError("Failed to get quizz model by id") from e

        if quizz_model is None:
            raise ItemNotFound("Quizz not found")
        
        return quizz_model

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
            quizz_models = result.scalars().all()
        except SQLAlchemyError as exc:
            logger.exception("Failed to get all quizz models")
            raise DatabaseError("Failed to get all quizz models") from exc
        except Exception as e:
            logger.exception("Failed to get all quizz models")
            raise DatabaseError("Failed to get all quizz models") from e
        
        if quizz_models is None:
            raise ItemNotFound("Quizzes not found")

        if len(quizz_models) == 0:
            raise ItemNotFound("Quizzes not found")
        
        return quizz_models

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
        except IntegrityError as exc:
            logger.exception("Failed to add quizz: %s", name)
            raise DatabaseError("Quizz with this name already exists") from exc
        except SQLAlchemyError as exc:
            logger.exception("Failed to add quizz: %s", name)
            raise DatabaseError("Failed to add quizz") from exc
        except Exception as e:
            logger.exception("Failed to add quizz: %s", name)
            raise DatabaseError("Failed to add quizz") from e
        
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
        quizz_model = await self.get_quizz_model_by_id(
            id,
            user_id
        )
        
        quizz_model.name = name or quizz_model.name
        quizz_model.description = description or quizz_model.description
        quizz_model.user_id = user_id or quizz_model.user_id
        try:
            await self.db.merge(quizz_model)
        except SQLAlchemyError as exc:
            logger.exception("Failed to update quizz: %s", id)
            raise DatabaseError("Failed to update quizz") from exc
        except Exception as e:
            logger.exception("Failed to update quizz: %s", id)
            raise DatabaseError("Failed to update quizz") from e
        
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
        quizz_model = await self.get_quizz_model_by_id(
            id,
            user_id
        )
     
        quizz_model.soft_delete()
        try:
            await self.db.merge(quizz_model)
        except SQLAlchemyError as exc:
            logger.exception("Failed to delete quizz: %s", id)
            raise DatabaseError("Failed to delete quizz") from exc
        except Exception as e:
            logger.exception("Failed to delete quizz: %s", id)
            raise DatabaseError("Failed to delete quizz") from e
        
        return True
