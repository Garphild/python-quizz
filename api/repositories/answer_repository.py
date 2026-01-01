import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from providers.models.answer_model import AnswerModel
from errors.database_error import DatabaseError
from errors.item_not_found import ItemNotFound
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

logger = logging.getLogger(__name__)

class AnswerRepository:
    db: AsyncSession | None = None
    
    def __init__(self, db: AsyncSession):
        self.db = db

        if self.db is None:
            raise DatabaseError("Database session is not initialized")

    '''
    Get all answers by question id
    @param quizz_id: int
    @param question_id: int
    @param user_id: int
    @return: list[AnswerModel]
    '''
    async def get_answers_by_question_id(
        self,
        quizz_id: int,
        question_id: int,
        user_id: int,
    ) -> list[AnswerModel]:
        stmt = select(AnswerModel).filter(
            AnswerModel.question_id == question_id,
            AnswerModel.deleted_at.is_(None),
            AnswerModel.user_id == user_id,
            AnswerModel.quizz_id == quizz_id
        )
        try:
            result = await self.db.execute(stmt)
            answers = result.scalars().all()
        except SQLAlchemyError as exc:
            logger.exception("Failed to get answers by question id")
            raise DatabaseError("Failed to get answers by question id") from exc

        if not answers:
            raise ItemNotFound("Answers not found")

        return answers

    '''
    Get answer by Id
    @param quizz_id: int
    @param question_id: int
    @param answer_id: int
    @param user_id: int
    @return: AnswerModel
    '''
    async def get_answer_by_id(
        self,
        quizz_id: int,
        question_id: int,
        answer_id: int,
        user_id: int,
    ) -> AnswerModel:        
        stmt = select(AnswerModel).filter(
            AnswerModel.id == answer_id,
            AnswerModel.deleted_at.is_(None),
            AnswerModel.user_id == user_id,
            AnswerModel.quizz_id == quizz_id,
            AnswerModel.question_id == question_id
        )
        try:
            result = await self.db.execute(stmt)
            answer = result.scalar_one_or_none()
        except SQLAlchemyError as exc:
            logger.exception("Failed to get answer by id")
            raise DatabaseError("Failed to get answer by id") from exc

        if answer is None:
            raise ItemNotFound("Answer not found")

        return answer

    '''
    Create new answer
    @param text: str
    @param is_correct: bool
    @param question_id: int
    @return: AnswerModel
    @throws: DatabaseError    
    '''
    async def add(
        self,
        text: str,
        is_correct: bool,
        question_id: int,
    ) -> AnswerModel:
        answer_model = AnswerModel()
        answer_model.answer_text = text
        answer_model.is_correct = is_correct
        answer_model.question_id = question_id

        try:
            await self.db.add(answer_model)
        except IntegrityError as exc:
            logger.exception("Failed to add answer (duplicate?)")
            raise DatabaseError("Answer with this text already exists") from exc
        except SQLAlchemyError as exc:
            logger.exception("Failed to add answer")
            raise DatabaseError("Failed to add answer") from exc

        return answer_model

    '''
    Update existing answer
    @param quizz_id: int,
    @param question_id: int,
    @param answer_id: int,
    @param user_id: int,
    @param text: str | None = None,
    @param is_correct: bool | None = None,
    @return: AnswerModel
    @throws: ItemNotFound
    @throws: DatabaseError
    '''    
    async def update(
        self,
        quizz_id: int,
        question_id: int,
        answer_id: int,
        user_id: int,
        text: str | None = None,
        is_correct: bool | None = None,
    ) -> AnswerModel:
        answer_model = await self.get_answer_by_id(
            quizz_id,
            question_id,
            answer_id,
            user_id
        )
        
        if answer_model is None:
            raise ItemNotFound("Answer not found")
        
        if text is not None:
            answer_model.answer_text = text
        
        if is_correct is not None:
            answer_model.is_correct = is_correct
        
        try:
            await self.db.merge(answer_model)
        except SQLAlchemyError as exc:
            logger.exception("Failed to update answer")
            raise DatabaseError("Failed to update answer") from exc
        
        return answer_model

    '''
    Delete answer
    @param answer_id: int
    @param quizz_id: int
    @return: bool
    @throws: ItemNotFound
    @throws: DatabaseError
    '''
    async def delete(
        self,
        answer_id: int,
        quizz_id: int,
        question_id: int,
        user_id: int,
    ) -> bool:
        answer_model = await self.get_answer_by_id(
            quizz_id,
            question_id,
            answer_id,
            user_id
        )

        answer_model.soft_delete()
        try:
            await self.db.merge(answer_model)
        except SQLAlchemyError as exc:
            logger.exception("Failed to delete answer")
            raise DatabaseError("Failed to delete answer") from exc
        
        return True
