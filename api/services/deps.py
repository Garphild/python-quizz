from fastapi import Request
from services.user_service import UserService
from services.quizz_service import QuizzService
from services.question_service import QuestionsService
from services.answer_service import AnswerService
from repositories.user_repository import UserRepository
from repositories.quizz_repository import QuizzRepository
from repositories.question_repository import QuestionRepository
from repositories.answer_repository import AnswerRepository

def get_user_service(request: Request):
    db = request.app.state.db_sessionmaker()
    user_repository = UserRepository(db)
    return UserService(user_repository) 

def get_quizz_service(request: Request):
    db = request.app.state.db_sessionmaker()
    quizz_repository = QuizzRepository(db)
    return QuizzService(quizz_repository) 

def get_questions_service(request: Request):
    db = request.app.state.db_sessionmaker()
    question_repository = QuestionRepository(db)
    return QuestionsService(question_repository) 

def get_answer_service(request: Request):
    db = request.app.state.db_sessionmaker()
    answer_repository = AnswerRepository(db)
    return AnswerService(answer_repository) 