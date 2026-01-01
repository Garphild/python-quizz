from fastapi import Request
from services.user_service import UserService
from services.quizz_service import QuizzService
from services.question_service import QuestionsService
from services.answer_service import AnswerService

def get_user_service(request: Request):
    return UserService(request.state.db_sessionmaker()) 

def get_quizz_service(request: Request):
    return QuizzService(request.state.db_sessionmaker()) 

def get_questions_service(request: Request):
    return QuestionsService(request.state.db_sessionmaker()) 

def get_answer_service(request: Request):
    return AnswerService(request.state.db_sessionmaker()) 