from providers.models.question_model import QuestionModel
from fastapi import Depends
from repositories.deps import get_question_repository
from repositories.question_repository import QuestionRepository

class QuestionsService:
    question_repository: QuestionRepository | None = None
    
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository
    
    async def get_questions(
        self,
        quizz_id: int,
        user_id: int,
    ) -> list[QuestionModel]:
        questions = await self.question_repository.get_all_questions(quizz_id, user_id)
        if not questions:
            raise Exception("Questions not found")

        return questions
    
    async def get_question_by_id(
        self,
        quizz_id: int,
        question_id: int,
        user_id: int,
    ) -> QuestionModel:
        question = await self.question_repository.get_question_by_id(quizz_id, question_id, user_id)
        if not question:
            raise Exception("Question not found")

        return question

    async def create_question(
        self,
        quizz_id: int,
        question_text: str,
        user_id: int,
    ) -> QuestionModel:
        question = await self.question_repository.add(quizz_id, question_text, user_id)
        if not question:
            raise Exception("Question not found")

        return question

    async def update_question(
        self,
        quizz_id: int,
        question_id: int,
        question_text: str,
        user_id: int,
    ) -> QuestionModel:
        question = await self.question_repository.update(quizz_id, question_id, question_text, user_id)
        if not question:
            raise Exception("Question not found")

        return question

    async def delete_question(
        self,
        quizz_id: int,
        question_id: int,
        user_id: int,
    ) -> bool:
        return await self.question_repository.delete(quizz_id, question_id, user_id)