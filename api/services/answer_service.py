from providers.models.answer_model import AnswerModel
from fastapi import Depends
from repositories.answer_repository import AnswerRepository
from repositories.deps import get_answer_repository


class AnswerService:
    async def get_answers_by_question_id(
        self,
        question_id: int,
        answer_repository: AnswerRepository = Depends(get_answer_repository)
    ) -> list[AnswerModel]:
        answers = await answer_repository.get_answers_by_question_id(question_id)
        if not answers:
            raise Exception("Answers not found")

        return [AnswerModel.from_orm(answer) for answer in answers]

    async def get_answer_by_id(
        self,
        answer_id: int,
        answer_repository: AnswerRepository = Depends(get_answer_repository)
    ) -> AnswerModel:
        answer = await answer_repository.get_answer_by_id(answer_id)
        if not answer:
            raise Exception("Answer not found")

        return AnswerModel.from_orm(answer)

    async def add(
        self,
        text: str,
        is_correct: bool,
        user_id: int,
        description: str,
        quizz_id: int,
        question_id: int,
        answer_repository: AnswerRepository = Depends(get_answer_repository)
    ) -> AnswerModel:
        answer = await answer_repository.add(text, is_correct, user_id, description, quizz_id, question_id)
        if not answer:
            raise Exception("Answer not found")

        return AnswerModel.from_orm(answer)

    async def update(
        self,
        answer_id: int,
        text: str,
        is_correct: bool,
        description: str,
        answer_repository: AnswerRepository = Depends(get_answer_repository)
    ) -> AnswerModel:
        answer = await answer_repository.update(answer_id, text, is_correct, description)
        if not answer:
            raise Exception("Answer not found")

        return AnswerModel.from_orm(answer)

    async def delete(
        self,
        answer_id: int,
        answer_repository: AnswerRepository = Depends(get_answer_repository)
    ) -> bool:
        result = await answer_repository.delete(answer_id)
        if not result:
            return False

        return True
