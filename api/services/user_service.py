from providers.models.user_model import UserModel
from providers.postgree_provider import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

from routes.auth.dto.auth_dto import RegisterRequest
from routes.auth.dto.profile_dto import ProfileDto

class UserService:
    async def get_by_email(self, email: str, db: Session = Depends(get_db)) -> ProfileDto | None:
        try:
            user = db.query(UserModel).filter(UserModel.email == email).first()

            if user is None:
                return None

            return ProfileDto.model_validate(user)
        except Exception:
            return None
        finally:
            db.close()

    
    async def create_user(self, user: RegisterRequest, db: Session = Depends(get_db)) -> ProfileDto:
        try:
            user_model = UserModel(
                email=user.email,
                name=user.name,
                surname=user.surname or "",
                password=bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            )

            db.add(user_model)
            db.commit()
            db.refresh(user_model)

            return ProfileDto.model_validate(user_model)
        except Exception:
            return None
        finally:
            db.close()
        
    

    async def update_user(self, user_id: int, user_data: RegisterRequest, db: Session = Depends(get_db)) -> ProfileDto | None:
        try:
            user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
            if user_model is None:
                return None
            
            user_model.email = user_data.email
            user_model.name = user_data.name
            user_model.surname = user_data.surname or ""
            user_model.password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            db.commit()
            db.refresh(user_model)
            return ProfileDto.model_validate(user_model)
        except Exception:
            return None
        finally:
            db.close()

    async def delete_user(self, user_id: int, db: Session = Depends(get_db)) -> bool:
        try:
            user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
            if user_model is None:
                return False
            
            db.delete(user_model)
            db.commit()
            return True
        except Exception:
            return False
        finally:
            db.close()