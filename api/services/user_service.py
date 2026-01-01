import bcrypt
from providers.models.user_model import UserModel
from fastapi import Depends
from routes.dto.auth_dto import RegisterRequestDto
from repositories.user_repository import UserRepository
from repositories.deps import get_user_repository
from errors.invalid_credentials import InvalidCredentials
from errors.item_not_found import ItemNotFound

class UserService:
    async def get_user_model_by_email(
        self,
        email: str,
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> UserModel:
        user = await user_repository.get_user_model_by_email(email)
        if user is None:
            raise ItemNotFound("User not found")

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
        if user is None:
            raise ItemNotFound("User not found")

        return user

    async def create_user(
        self,
        user: RegisterRequestDto,
        user_repository: UserRepository = Depends(get_user_repository)
    ) -> UserModel:
        hashed = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        if hashed is None:
            raise Exception("Failed to hash password")

        surname = user.surname or ""
        if user.name is None:
            raise Exception("Name is required")
        if user.email is None:
            raise Exception("Email is required")

        user_model = await user_repository.add(user.email, user.name, surname, hashed)

        await user_repository.db.commit()
        await user_repository.db.refresh(user_model)
        return user_model

    async def update_password(
        self,
        user_id: int,
        new_password: str,
        userRepository: UserRepository = Depends(get_user_repository)
    ) -> bool:
        user_model = await userRepository.get_user_model_by_id(user_id)
        if user_model is None:
            raise ItemNotFound("User not found")
        
        user_model.set_password(new_password)
        await userRepository.update(password=new_password, id=user_id)

        await userRepository.db.commit()
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

        await userRepository.db.commit()
        await userRepository.db.refresh(user_model)
        return user_model

    async def delete_user(
        self,
        user_id: int,
        userRepository: UserRepository = Depends(get_user_repository)
    ) -> bool:
        result = await userRepository.delete(user_id)
        if not result:
            return False

        await userRepository.db.commit()
        return True

user_service = UserService()