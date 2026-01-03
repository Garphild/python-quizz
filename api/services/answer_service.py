from providers.models.answer_model import AnswerModel
from repositories.answer_repository import AnswerRepository


class AnswerService:
    answer_repository: AnswerRepository | None = None
    
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository
    
    async def get_answers_by_question_id(
        self,
        question_id: int,
    ) -> list[AnswerModel]:
        answers = await self.answer_repository.get_answers_by_question_id(question_id)

        return answers

    async def get_answer_by_id(
        self,
        answer_id: int,
    ) -> AnswerModel:
        answer = await self.answer_repository.get_answer_by_id(answer_id)

        return answer

    async def add(
        self,
        text: str,
        is_correct: bool,
        user_id: int,
        description: str,
        quizz_id: int,
        question_id: int,
    ) -> AnswerModel:
        answer = await self.answer_repository.add(text, is_correct, user_id, description, quizz_id, question_id)

        return answer

    async def update(
        self,
        answer_id: int,
        text: str,
        is_correct: bool,
        description: str,
    ) -> AnswerModel:
        answer = await self.answer_repository.update(answer_id, text, is_correct, description)

        return answer

    async def delete(
        self,
        answer_id: int,
    ) -> bool:
        result = await self.answer_repository.delete(answer_id)

        return result
