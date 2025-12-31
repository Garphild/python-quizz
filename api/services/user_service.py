from api.repositories.user_repository import UserRepository, get_user_repository
import bcrypt
from providers.models.user_model import UserModel
from providers.postgree_provider import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

from routes.dto.auth_dto import RegisterRequestDto, ProfileDto

class UserService:
    async def get_by_email(self, email: str, userRepository: UserRepository = Depends(get_user_repository)) -> ProfileDto | None:
        try:
            user = userRepository.get_user_model_by_email(email)

            if user is None:
                return None

            return ProfileDto.model_validate(user)
        except Exception:
            return None

    async def get_user_model_by_email(self, email: str, userRepository: UserRepository = Depends(get_user_repository)) -> UserModel | None:
        try:
            return userRepository.get_user_model_by_email(email)
        except Exception:
            return None

    async def verify_login(self, email: str, password: str, userRepository: UserRepository = Depends(get_user_repository)) -> ProfileDto | None:
        try:
            user = userRepository.get_user_model_by_email(email)
            if user is None:
                return None
            is_valid = user.verify_password(password)
            if not is_valid:
                return None
            return ProfileDto.model_validate(user)
        except Exception as e:
            return None

    async def get_by_id(self, id: int, db: Session = Depends(get_db)) -> UserModel | None:
        try:
            return db.query(UserModel).filter(UserModel.id == id).first()
        except Exception:
            return None

    async def create_user(self, user: RegisterRequestDto, db: Session = Depends(get_db)) -> ProfileDto | None:
        try:
            # Hash password first
            hashed = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            user_model = UserModel(
                email=user.email,
                name=user.name,
                surname=user.surname or "",
                password=hashed
            )

            db.add(user_model)
            db.commit()
            db.refresh(user_model)

            return ProfileDto.model_validate(user_model)
        except Exception:
            db.rollback()
            return None
        
    

    async def update_password(self, user_id: int, new_password: str, db: Session = Depends(get_db)) -> bool:
        try:
            user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
            if user_model is None:
                return False
            
            user_model.set_password(new_password)
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

    async def update_profile(self, user_id: int, data, db: Session = Depends(get_db)) -> ProfileDto | None:
        try:
            user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
            if user_model is None:
                return None
            
            if data.name is not None:
                user_model.name = data.name
            if data.surname is not None:
                user_model.surname = data.surname
            
            db.commit()
            db.refresh(user_model)
            return ProfileDto.model_validate(user_model)
        except Exception:
            db.rollback()
            return None

    async def delete_user(self, user_id: int, db: Session = Depends(get_db)) -> bool:
        try:
            user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
            if user_model is None:
                return False
            
            db.delete(user_model)
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

user_service = UserService()