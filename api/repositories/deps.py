from fastapi import Request
from repositories.user_repository import UserRepository
from repositories.quizz_repository import QuizzRepository
from repositories.question_repository import QuestionRepository
from repositories.answer_repository import AnswerRepository

def get_user_repository(request: Request):
    return UserRepository(request.state.db_sessionmaker())

def get_quizz_repository(request: Request):
    return QuizzRepository(request.state.db_sessionmaker())

def get_question_repository(request: Request):
    return QuestionRepository(request.state.db_sessionmaker())

def get_answer_repository(request: Request):
    return AnswerRepository(request.state.db_sessionmaker())