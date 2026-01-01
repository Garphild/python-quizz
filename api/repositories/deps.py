from fastapi import Request
from repositories.user_repository import UserRepository
from repositories.quizz_repository import QuizzRepository
from repositories.question_repository import QuestionRepository
from repositories.answer_repository import AnswerRepository

async def get_user_repository(request: Request):
    db = await request.state.db_sessionmaker()
    return UserRepository(db)

async def get_quizz_repository(request: Request):
    db = await request.state.db_sessionmaker()
    return QuizzRepository(db)

async def get_question_repository(request: Request):
    db = await request.state.db_sessionmaker()
    return QuestionRepository(db)

async def get_answer_repository(request: Request):
    db = await request.state.db_sessionmaker()
    return AnswerRepository(db)