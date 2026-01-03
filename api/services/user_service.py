import bcrypt
from providers.models.user_model import UserModel
from repositories.user_repository import UserRepository
from errors.invalid_credentials import InvalidCredentials
from errors.database_error import DatabaseError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class UserService:
    user_repository: UserRepository | None = None
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def get_user_model_by_email(
        self,
        email: str,
    ) -> UserModel | None:
        user = await self.user_repository.get_user_model_by_email(email)

        return user

    async def verify_login(
        self,
        email: str,
        password: str,
    ) -> bool:
        user = await self.user_repository.get_user_model_by_email(email)

        return user.verify_password(password)

    async def get_user_model_by_id(
        self,
        id: int,
    ) -> UserModel:
        user = await self.user_repository.get_user_model_by_id(id)

        return user

    async def create_user(
        self,
        password: str,
        email: str,
        name: str,
        surname: str,
    ) -> UserModel:
        if password is None:
            raise Exception("Password is required")

        if len(password) < 8:
            raise Exception("Password must be at least 8 characters long")
        
        if email is None:
            raise Exception("Email is required")
        
        if name is None:
            raise Exception("Name is required")
        
        if surname is None:
            raise Exception("Surname is required")
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user_model = await self.user_repository.add(email, name, surname, hashed)

        if user_model is None:
            raise DatabaseError("Failed to create user")

        try:
            await self.user_repository.db.commit()
            await self.user_repository.db.refresh(user_model)
        except IntegrityError as exc:
            await self.user_repository.db.rollback()
            raise DatabaseError("User with this email already exists") from exc
        except SQLAlchemyError as exc:
            await self.user_repository.db.rollback()
            raise DatabaseError("Failed to create user") from exc

        return user_model

    async def update_password(
        self,
        user_id: int,
        new_password: str,
    ) -> bool:
        user_model = await self.user_repository.get_user_model_by_id(user_id)
        
        if user_model is None:
            raise DatabaseError("User not found")
        
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            await self.user_repository.update(password=hashed, id=user_id)
            await self.user_repository.db.commit()
        except SQLAlchemyError as exc:
            await self.user_repository.db.rollback()
            raise DatabaseError("Failed to update password") from exc

        return True

    async def update_profile(
        self,
        user_id: int,
        data,
    ) -> UserModel | None:
        user_model = await self.user_repository.update(
            id=user_id,
            name=data.name,
            surname=data.surname,
            email=data.email
        )

        if user_model is None:
            return None

        try:
            await self.user_repository.db.commit()
            await self.user_repository.db.refresh(user_model)
        except SQLAlchemyError as exc:
            await self.user_repository.db.rollback()
            raise DatabaseError("Failed to update profile") from exc

        return user_model

    async def delete_user(
        self,
        user_id: int,
    ) -> bool:
        user_model = await self.user_repository.get_user_model_by_id(user_id)
        
        if user_model is None:
            raise DatabaseError("User not found")

        await self.user_repository.delete(user_id)

        try:
            await self.user_repository.db.commit()
        except SQLAlchemyError as exc:
            await self.user_repository.db.rollback()
            raise DatabaseError("Failed to delete user") from exc

        return True

