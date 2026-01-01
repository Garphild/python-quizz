from routes.dto.quizz_dto import QuizzDto, CreateQuizzDto, UpdateQuizzDto
from fastapi import Depends
from repositories.deps import get_quizz_repository
from repositories.quizz_repository import QuizzRepository

class QuizzService:
    async def get_all(self, user_id: int, quizz_repository: QuizzRepository = Depends(get_quizz_repository)) -> list[QuizzDto]:
        try:
            quizz_models = await quizz_repository.get_all_quizz_models(user_id)
            return [QuizzDto.from_orm(quizz_model) for quizz_model in quizz_models]
        except Exception:
            return []
    
    async def get_by_id(self, quizz_id: int, user_id: int, quizz_repository: QuizzRepository = Depends(get_quizz_repository)) -> QuizzDto:
        try:
            quizz_model = await quizz_repository.get_quizz_model_by_id(quizz_id, user_id)
            return QuizzDto.from_orm(quizz_model)
        except Exception:
            return None
    
    async def create(self, user_id: int, quizz: CreateQuizzDto, quizz_repository: QuizzRepository = Depends(get_quizz_repository)) -> QuizzDto:
        try:
            quizz_model = await quizz_repository.add(quizz.name, quizz.description, user_id, quizz.url)

            await quizz_repository.db.commit()
            await quizz_repository.db.refresh(quizz_model)

            return QuizzDto.from_orm(quizz_model)
        except Exception:
            await quizz_repository.db.rollback()
            return None
    
    async def update(self, quizz_id: int, quizz: UpdateQuizzDto, user_id: int, quizz_repository: QuizzRepository = Depends(get_quizz_repository)) -> QuizzDto:
        try:
            quizz_model = await quizz_repository.update(quizz_id, quizz.name, quizz.description, user_id)

            await quizz_repository.db.commit()
            await quizz_repository.db.refresh(quizz_model)

            return QuizzDto.from_orm(quizz_model)
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