import bcrypt
from providers.models.user_model import UserModel
from fastapi import Depends
from repositories.user_repository import UserRepository
from repositories.deps import get_user_repository
from errors.invalid_credentials import InvalidCredentials
from errors.database_error import DatabaseError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class UserService:
    async def get_user_model_by_email(
        self,
        email: str,
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> UserModel:
        user = await user_repository.get_user_model_by_email(email)

        return user

    async def verify_login(
        self,
        email: str,
        password: str,
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> UserModel:
        user = await user_repository.get_user_model_by_email(email)

        is_valid = user.verify_password(password)

        if not is_valid:
            raise InvalidCredentials("Invalid credentials")

        return user

    async def get_user_model_by_id(
        self,
        id: int,
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> UserModel:
        user = await user_repository.get_user_model_by_id(id)

        return user

    async def create_user(
        self,
        password: str,
        email: str,
        name: str,
        surname: str,
        user_repository: UserRepository = Depends(get_user_repository)
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

        user_model = await user_repository.add(email, name, surname, hashed)

        try:
            await user_repository.db.commit()
            await user_repository.db.refresh(user_model)
        except IntegrityError as exc:
            await user_repository.db.rollback()
            raise DatabaseError("User with this email already exists") from exc
        except SQLAlchemyError as exc:
            await user_repository.db.rollback()
            raise DatabaseError("Failed to create user") from exc

        return user_model

    async def update_password(
        self,
        user_id: int,
        new_password: str,
        userRepository: UserRepository = Depends(get_user_repository)
    ) -> bool:
        await userRepository.get_user_model_by_id(user_id)
        
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            await userRepository.update(password=hashed, id=user_id)
            await userRepository.db.commit()
        except SQLAlchemyError as exc:
            await userRepository.db.rollback()
            raise DatabaseError("Failed to update password") from exc

        return True

    async def update_profile(
        self,
        user_id: int,
        data,
        userRepository: UserRepository = Depends(get_user_repository)
    ) -> UserModel | None:
        user_model = await userRepository.update(
            id=user_id,
            name=data.name,
            surname=data.surname,
            email=data.email
        )

        if user_model is None:
            return None

        try:
            await userRepository.db.commit()
            await userRepository.db.refresh(user_model)
        except SQLAlchemyError as exc:
            await userRepository.db.rollback()
            raise DatabaseError("Failed to update profile") from exc

        return user_model

    async def delete_user(
        self,
        user_id: int,
        userRepository: UserRepository = Depends(get_user_repository)
    ) -> bool:
        await userRepository.delete(user_id)

        try:
            await userRepository.db.commit()
        except SQLAlchemyError as exc:
            await userRepository.db.rollback()
            raise DatabaseError("Failed to delete user") from exc

        return True

