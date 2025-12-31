import bcrypt
from providers.models.user_model import UserModel
from fastapi import Depends
from routes.dto.auth_dto import RegisterRequestDto
from repositories.user_repository import UserRepository
from repositories.deps import get_user_repository

class UserService:
    async def get_user_model_by_email(
        self,
        email: str,
        userRepository: UserRepository = Depends(get_user_repository)
    ) -> UserModel | None:
        try:
            user = await userRepository.get_user_model_by_email(email)
        except Exception:
            return None
        else:
            return user

    async def verify_login(
        self,
        email: str,
        password: str,
        userRepository: UserRepository = Depends(get_user_repository)
    ) -> UserModel | None:
        try:
            user = await userRepository.get_user_model_by_email(email)

            is_valid = user.verify_password(password)

            if not is_valid:
                raise Exception("Invalid credentials")
        except Exception:
            return None
        else:
            return user

    async def get_user_model_by_id(
        self,
        id: int,
        userRepository: UserRepository = Depends(get_user_repository)
    ) -> UserModel | None:
        try:
            user = await userRepository.get_user_model_by_id(id)
            if user is None:
                raise Exception("User not found")
        except Exception:
            return None
        else:
            return user

    async def create_user(
        self,
        user: RegisterRequestDto,
        userRepository: UserRepository = Depends(get_user_repository)
    ) -> UserModel | None:
        try:
            hashed = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            if hashed is None:
                raise Exception("Failed to hash password")

            surname = user.surname or ""
            if user.name is None:
                raise Exception("Name is required")
            if user.email is None:
                raise Exception("Email is required")

            user_model = await userRepository.add(user.email, user.name, surname, hashed)

            await userRepository.db.commit()
            await userRepository.db.refresh(user_model)
            return user_model
        except Exception:
            await userRepository.db.rollback()
            return None

    async def update_password(
        self,
        user_id: int,
        new_password: str,
        userRepository: UserRepository = Depends(get_user_repository)
    ) -> bool:
        try:
            user_model = await userRepository.get_user_model_by_id(user_id)
            if user_model is None:
                return False
            
            user_model.set_password(new_password)
            await userRepository.update(password=new_password, id=user_id)

            await userRepository.db.commit()
            return True
        except Exception:
            await userRepository.db.rollback()
            return False

    async def update_profile(
        self,
        user_id: int,
        data,
        userRepository: UserRepository = Depends(get_user_repository)
    ) -> UserModel | None:
        try:
            user_model = await userRepository.update(
                id=user_id,
                name=data.name,
                surname=data.surname,
                email=data.email
            )

            if user_model is None:
                return None

            await userRepository.db.commit()
            await userRepository.db.refresh(user_model)
            return user_model
        except Exception:
            await userRepository.db.rollback()
            return None

    async def delete_user(
        self,
        user_id: int,
        userRepository: UserRepository = Depends(get_user_repository)
    ) -> bool:
        try:
            result = await userRepository.delete(user_id)
            if not result:
                return False

            await userRepository.db.commit()
            return True
        except Exception:
            await userRepository.db.rollback()
            return False

user_service = UserService()