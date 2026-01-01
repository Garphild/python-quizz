from providers.models.question_model import QuestionModel
from fastapi import Depends
from repositories.deps import get_question_repository
from repositories.question_repository import QuestionRepository

class QuestionsService:
    async def get_questions(
        self,
        quizz_id: int,
        user_id: int,
        question_repository: QuestionRepository = Depends(get_question_repository)
    ) -> list[QuestionModel]:
        questions = await question_repository.get_all_questions(quizz_id, user_id)
        if not questions:
            raise Exception("Questions not found")

        return questions
    
    async def get_question_by_id(
        self,
        quizz_id: int,
        question_id: int,
        user_id: int,
        question_repository: QuestionRepository = Depends(get_question_repository)
    ) -> QuestionModel:
        question = await question_repository.get_question_by_id(quizz_id, question_id, user_id)
        if not question:
            raise Exception("Question not found")

        return question

    async def create_question(
        self,
        quizz_id: int,
        question_text: str,
        user_id: int,
        question_repository: QuestionRepository = Depends(get_question_repository)
    ) -> QuestionModel:
        question = await question_repository.add(quizz_id, question_text, user_id)
        if not question:
            raise Exception("Question not found")

        return question

    async def update_question(
        self,
        quizz_id: int,
        question_id: int,
        question_text: str,
        user_id: int,
        question_repository: QuestionRepository = Depends(get_question_repository)
    ) -> QuestionModel:
        question = await question_repository.update(quizz_id, question_id, question_text, user_id)
        if not question:
            raise Exception("Question not found")

        return question

    async def delete_question(
        self,
        quizz_id: int,
        question_id: int,
        user_id: int,
        question_repository: QuestionRepository = Depends(get_question_repository)
    ) -> bool:
        return await question_repository.delete(quizz_id, question_id, user_id)