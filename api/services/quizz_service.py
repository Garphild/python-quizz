from fastapi import Depends
from repositories.deps import get_quizz_repository
from repositories.quizz_repository import QuizzRepository
from providers.models.quizz_model import QuizzModel

class QuizzService:
    async def get_all(self, user_id: int, quizz_repository: QuizzRepository = Depends(get_quizz_repository)) -> list[QuizzModel]:
        try:
            quizz_models = await quizz_repository.get_all_quizz_models(user_id)
            return quizz_models
        except Exception:
            return []
    
    async def get_by_id(self, quizz_id: int, user_id: int, quizz_repository: QuizzRepository = Depends(get_quizz_repository)) -> QuizzModel:
        try:
            quizz_model = await quizz_repository.get_quizz_model_by_id(quizz_id, user_id)
            return quizz_model
        except Exception:
            return None
    
    async def create(self, user_id: int, name: str, description: str, url: str, quizz_repository: QuizzRepository = Depends(get_quizz_repository)) -> QuizzModel:
        try:
            quizz_model = await quizz_repository.add(name, description, user_id, url)

            await quizz_repository.db.commit()
            await quizz_repository.db.refresh(quizz_model)

            return quizz_model
        except Exception:
            await quizz_repository.db.rollback()
            return None
    
    async def update(self, quizz_id: int, name: str, description: str, user_id: int, quizz_repository: QuizzRepository = Depends(get_quizz_repository)) -> QuizzModel:
        try:
            quizz_model = await quizz_repository.update(quizz_id, name, description, user_id)

            await quizz_repository.db.commit()
            await quizz_repository.db.refresh(quizz_model)

            return quizz_model
        except Exception:
            await quizz_repository.db.rollback()
            return None
    
    async def delete(self, quizz_id: int, user_id: int, quizz_repository: QuizzRepository = Depends(get_quizz_repository)) -> bool:
        try:
            result = await quizz_repository.delete(quizz_id)

            await quizz_repository.db.commit()
            return result
        except Exception:
            await quizz_repository.db.rollback()
            return False

quizz_service = QuizzService()