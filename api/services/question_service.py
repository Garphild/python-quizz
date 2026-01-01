from entities.questions import Question
from fastapi import Depends
from repositories.deps import get_question_repository
from repositories.question_repository import QuestionRepository

class QuestionsService:
    async def get_questions(
        self,
        quizz_id: int,
        user_id: int,
        question_repository: QuestionRepository = Depends(get_question_repository)
    ) -> list[Question]:
        questions = await question_repository.get_all_questions(quizz_id, user_id)
        if not questions:
            raise Exception("Questions not found")

        return [Question.from_orm(question) for question in questions]
    
    async def get_question_by_id(
        self,
        quizz_id: int,
        question_id: int,
        user_id: int,
        question_repository: QuestionRepository = Depends(get_question_repository)
    ) -> Question:
        question = await question_repository.get_question_by_id(quizz_id, question_id, user_id)
        if not question:
            raise Exception("Question not found")

        return Question.from_orm(question)

    async def create_question(
        self,
        quizz_id: int,
        question: Question,
        user_id: int,
        question_repository: QuestionRepository = Depends(get_question_repository)
    ) -> Question:
        question = await question_repository.add(quizz_id, question.text, user_id)
        if not question:
            raise Exception("Question not found")

        return Question.from_orm(question)

    async def update_question(
        self,
        quizz_id: int,
        question_id: int,
        question: Question,
        user_id: int,
        question_repository: QuestionRepository = Depends(get_question_repository)
    ) -> Question:
        question = await question_repository.update(quizz_id, question_id, question.text, user_id)
        if not question:
            raise Exception("Question not found")

        return Question.from_orm(question)

    async def delete_question(
        self,
        quizz_id: int,
        question_id: int,
        user_id: int,
        question_repository: QuestionRepository = Depends(get_question_repository)
    ) -> bool:
        return await question_repository.delete(quizz_id, question_id, user_id)