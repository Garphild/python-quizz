from entities.questions import Question

class QuestionsService:
    async def get_questions(self):
        return []
    
    async def get_question(self, question_id: int):
        return []

    async def create_question(self, question: Question):
        return []

    async def update_question(self, question_id: int, question: Question):
        return []

    async def delete_question(self, question_id: int):
        return []
    
    async def get_questions_by_quizz_id(self, quizz_id: int):
        return []

questionService = QuestionsService()