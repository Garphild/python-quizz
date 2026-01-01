from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from providers.models.question_model import QuestionModel
from errors.item_not_found import ItemNotFound
from errors.database_error import DatabaseError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging

logger = logging.getLogger(__name__)

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
        stmt = select(QuestionModel).filter(QuestionModel.quizz_id == quizz_id, QuestionModel.deleted_at.is_(None), QuestionModel.user_id == user_id)
        try:
            result = await self.db.execute(stmt)
            questions = result.scalars().all()
        except SQLAlchemyError as exc:
            logger.exception("Failed to get all questions")
            raise DatabaseError("Failed to get all questions") from exc

        if not questions:
            raise ItemNotFound("Questions not found")
        
        return questions
    
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
        stmt = select(QuestionModel).filter(
            QuestionModel.id == question_id,
            QuestionModel.deleted_at.is_(None),
            QuestionModel.user_id == user_id,
            QuestionModel.quizz_id == quizz_id
        )
        try:
            result = await self.db.execute(stmt)
            question = result.scalar_one_or_none()
        except SQLAlchemyError as exc:
            logger.exception("Failed to get question by id")
            raise DatabaseError("Failed to get question by id") from exc
        
        if question is None:
            raise ItemNotFound("Question not found")
        
        return question

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
        except IntegrityError as exc:
            logger.exception("Failed to add question (duplicate?)")
            raise DatabaseError("Question with this text already exists") from exc
        except SQLAlchemyError as exc:
            logger.exception("Failed to add question")
            raise DatabaseError("Failed to add question") from exc
        
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
        except SQLAlchemyError as exc:
            logger.exception("Failed to update question")
            raise DatabaseError("Failed to update question") from exc
        
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
        except SQLAlchemyError as exc:
            logger.exception("Failed to delete question")
            raise DatabaseError("Failed to delete question") from exc
        
        return True