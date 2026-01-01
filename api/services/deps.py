from fastapi import Request
from services.user_service import UserService
from services.quizz_service import QuizzService
from services.question_service import QuestionsService
from services.answer_service import AnswerService

async def get_user_service(request: Request):
    db = await request.state.db_sessionmaker()
    return UserService(db) 

async def get_quizz_service(request: Request):
    db = await request.state.db_sessionmaker()
    return QuizzService(db) 

async def get_questions_service(request: Request):
    db = await request.state.db_sessionmaker()
    return QuestionsService(db) 

async def get_answer_service(request: Request):
    db = await request.state.db_sessionmaker()
    return AnswerService(db) 