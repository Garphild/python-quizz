from fastapi import Depends
from repositories.deps import get_quizz_repository
from repositories.quizz_repository import QuizzRepository
from providers.models.quizz_model import QuizzModel

class QuizzService:   
    quizz_repository: QuizzRepository | None = None
    
    def __init__(self, quizz_repository: QuizzRepository):
        self.quizz_repository = quizz_repository
    
    async def get_all(self, user_id: int) -> list[QuizzModel]:
        try:
            quizz_models = await self.quizz_repository.get_all_quizz_models(user_id)
            return quizz_models
        except Exception:
            return []
    
    async def get_by_id(self, quizz_id: int, user_id: int) -> QuizzModel:
        try:
            quizz_model = await self.quizz_repository.get_quizz_model_by_id(quizz_id, user_id)
            return quizz_model
        except Exception:
            return None
    
    async def create(self, user_id: int, name: str, description: str, url: str) -> QuizzModel:
        try:
            quizz_model = await self.quizz_repository.add(name, description, user_id, url)

            await self.quizz_repository.db.commit()
            await self.quizz_repository.db.refresh(quizz_model)

            return quizz_model
        except Exception:
            await self.quizz_repository.db.rollback()
            return None
    
    async def update(self, quizz_id: int, name: str, description: str, user_id: int) -> QuizzModel:
        try:
            quizz_model = await self.quizz_repository.update(quizz_id, name, description, user_id)

            await self.quizz_repository.db.commit()
            await self.quizz_repository.db.refresh(quizz_model)

            return quizz_model
        except Exception:
            await self.quizz_repository.db.rollback()
            return None
    
    async def delete(self, quizz_id: int, user_id: int) -> bool:
        try:
            result = await self.quizz_repository.delete(quizz_id)

            await self.quizz_repository.db.commit()
            return result
        except Exception:
            await self.quizz_repository.db.rollback()
            return False