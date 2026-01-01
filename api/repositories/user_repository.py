import logging
from providers.models.user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from errors.database_error import DatabaseError
from errors.item_not_found import ItemNotFound

logger = logging.getLogger(__name__)

class UserRepository:
    db: AsyncSession | None = None
    
    def __init__(self, db: AsyncSession):
        self.db = db

        if self.db is None:
            raise DatabaseError("Database session is not initialized")

    '''
    Get user by email
    @param email: str
    @return: UserModel
    @throws: ItemNotFound
    '''    
    async def get_user_model_by_email(self, email: str) -> UserModel:
        try:
            stmt = select(UserModel).filter(UserModel.email == email, UserModel.deleted_at.is_(None))
            result = await self.db.execute(stmt)
            user = result.scalar_one_or_none()
        except SQLAlchemyError as exc:
            logger.exception("Failed to get user by email: %s", email)
            raise DatabaseError("Failed to get user by email") from exc

        if user is None:
            raise ItemNotFound("User not found")

        return user

    '''
    Get user by id
    @param id: int
    @return: UserModel
    @throws: ItemNotFound
    '''    
    async def get_user_model_by_id(self, id: int) -> UserModel:
        try:
            stmt = select(UserModel).filter(UserModel.id == id, UserModel.deleted_at.is_(None))
            result = await self.db.execute(stmt)
            user = result.scalar_one_or_none()
        except SQLAlchemyError as exc:
            logger.exception("Failed to get user by id: %s", id)
            raise DatabaseError("Failed to get user by id") from exc

        if user is None:
            raise ItemNotFound("User not found")

        return user

    '''
    Add new user
    @param email: str
    @param name: str
    @param surname: str
    @param password: str
    @return: UserModel
    '''    
    async def add(self, email: str, name: str, surname: str, password: str) -> UserModel:
        user_model = UserModel()
        user_model.email = email
        user_model.name = name
        user_model.surname = surname
        user_model.password = password

        try:
            self.db.add(user_model)
        except IntegrityError as exc:
            logger.exception("Duplicate email when adding user: %s", email)
            raise DatabaseError("User with this email already exists") from exc
        except SQLAlchemyError as exc:
            logger.exception("Failed to add user: %s", email)
            raise DatabaseError("Failed to add user") from exc
        except Exception as exc:
            logger.exception("Unexpected error when adding user: %s", email)
            raise DatabaseError("Failed to add user") from exc

        return user_model

    '''
    Delete user
    @param id: int
    @return: bool
    @throws: ItemNotFound
    '''    
    async def delete(self, id: int) -> bool:
        user_model = await self.get_user_model_by_id(id)

        try:
            user_model.soft_delete()
            await self.db.merge(user_model)
        except SQLAlchemyError as exc:
            logger.exception("Failed to delete user: %s", id)
            raise DatabaseError("Failed to delete user") from exc
        except Exception as exc:
            logger.exception("Unexpected error when deleting user: %s", id)
            raise DatabaseError("Failed to delete user") from exc

        return True


    '''
    Update user
    @param id: int
    @param email: str | None
    @param name: str | None
    @param surname: str | None
    @param password: str | None
    @return: UserModel
    @throws: ItemNotFound
    '''    
    async def update(
        self,
        id: int,
        email: str | None = None,
        name: str | None = None,
        surname: str | None = None,
        password: str | None = None,
    ) -> UserModel:
        user_model = await self.get_user_model_by_id(id)

        if password is not None:
            user_model.password = password

        if email is not None:
            user_model.email = email
        
        if name is not None:
            user_model.name = name
        
        if surname is not None:
            user_model.surname = surname
        
        try:
            await self.db.merge(user_model)
        except SQLAlchemyError as exc:
            logger.exception("Failed to update user: %s", id)
            raise DatabaseError("Failed to update user") from exc
        except Exception as exc:
            logger.exception("Unexpected error when updating user: %s", id)
            raise DatabaseError("Failed to update user") from exc

        return user_model
