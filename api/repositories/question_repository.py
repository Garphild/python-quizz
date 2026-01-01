from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from providers.models.question_model import QuestionModel
from errors.item_not_found import ItemNotFound
from errors.database_error import DatabaseError

class QuestionRepository:
    db: AsyncSession | None = None
    
    def __init__(self, db: AsyncSession):
        self.db = db

        if self.db is None:
            raise DatabaseError("Database session is not initialized")

    '''
    Get all questions by quizz id
    @param quizz_id: int
    @param user_id: int
    @return: list[QuestionModel]
    @throws: ItemNotFound
    '''    
    async def get_all_questions(
        self,
        quizz_id: int,
        user_id: int
    ) -> list[QuestionModel]:
        try:
            stmt = select(QuestionModel).filter(QuestionModel.quizz_id == quizz_id, QuestionModel.deleted_at.is_(None), QuestionModel.user_id == user_id)
            result = await self.db.execute(stmt)
            result = result.scalars().all()
        except Exception:
            raise DatabaseError("Failed to get all questions")

        if result is None:
            raise ItemNotFound("Questions not found")
        
        return result
    
    '''
    Get question by Id
    @param quizz_id: int
    @param question_id: int,
    @param user_id: int
    @return: QuestionModel
    @throws: ItemNotFound
    '''
    async def get_question_by_id(
        self,
        quizz_id: int,
        question_id: int,
        user_id: int
    ) -> QuestionModel:
        try:
            stmt = select(QuestionModel).filter(QuestionModel.id == question_id, QuestionModel.deleted_at.is_(None), QuestionModel.user_id == user_id, QuestionModel.quizz_id == quizz_id)
            result = await self.db.execute(stmt)
            result = result.scalar_one_or_none()
        except Exception:
            raise DatabaseError("Failed to get question by id")
        
        if result is None:
            raise ItemNotFound("Question not found")
        
        return result

    '''
    Create new question
    @param user_id: int
    @param quizz_id: int
    @param question_text: str
    @return: QuestionModel
    @throws: DatabaseError
    '''
    async def add(
        self,
        user_id: int,
        quizz_id: int,
        question_text: str
    ) -> QuestionModel:
        question = QuestionModel()
        question.user_id = user_id
        question.quizz_id = quizz_id
        question.question_text = question_text
        try:
            await self.db.add(question)
            await self.db.refresh(question)
        except Exception:
            raise DatabaseError("Failed to add question")
        
        return question

    '''
    Update existing question
    @param quizz_id: int,
    @param question_id: int,
    @param user_id: int,
    @param question_text: str
    @return: QuestionModel
    @throws: ItemNotFound
    @throws: DatabaseError
    '''    
    async def update(
        self,
        quizz_id: int,
        question_id: int,
        user_id: int,
        question_text: str
    ) -> QuestionModel:
        question = await self.get_question_by_id(quizz_id, question_id, user_id)
        
        question.question_text = question_text
        try:
            await self.db.merge(question)
            await self.db.refresh(question)
        except Exception:
            raise DatabaseError("Failed to update question")
        
        return question

    '''
    Delete question
    @param quizz_id: int,
    @param question_id: int,
    @param user_id: int
    @return: bool
    @throws: ItemNotFound
    @throws: DatabaseError
    '''
    async def delete(
        self,
        quizz_id: int,
        question_id: int,
        user_id: int
    ) -> bool:
        question = await self.get_question_by_id(quizz_id, question_id, user_id)
        
        question.soft_delete()
        try:
            await self.db.merge(question)
        except Exception:
            raise DatabaseError("Failed to delete question")
        
        return True