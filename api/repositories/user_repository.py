from providers.models.user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from errors.database_error import DatabaseError
from errors.item_not_found import ItemNotFound

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
            stmt = select(UserModel).filter(UserModel.email == email, UserModel.deleted_at.is_(None)).first()
            result = await self.db.execute(stmt)
            result = result.scalar()
        except Exception as e:
            raise DatabaseError.from_exc(e)

        if result is None:
            raise ItemNotFound("User not found")

        return result

    '''
    Get user by id
    @param id: int
    @return: UserModel
    @throws: ItemNotFound
    '''    
    async def get_user_model_by_id(self, id: int) -> UserModel:
        stmt = select(UserModel).filter(UserModel.id == id, UserModel.deleted_at.is_(None)).first()
        result = await self.db.execute(stmt)
        result = result.scalar()

        if result is None:
            raise ItemNotFound("User not found")

        return result

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

        self.db.add(user_model)

        return user_model

    '''
    Delete user
    @param id: int
    @return: bool
    @throws: ItemNotFound
    '''    
    async def delete(self, id: int) -> bool:
        user_model = await self.get_user_model_by_id(id)

        user_model.soft_delete()
        await self.db.merge(user_model)

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
        
        await self.db.merge(user_model)

        return user_model
