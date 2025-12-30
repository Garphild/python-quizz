from routes.dto.quizz_dto import QuizzDto, CreateQuizzDto, UpdateQuizzDto

class QuizzService:
    async def get_all(self) -> list[QuizzDto]:
        """Get all quizzes"""
        return []
    
    async def get_by_id(self, quizz_id: int) -> QuizzDto:
        """Get quiz by ID"""
        return None
    
    async def create(self, quizz: CreateQuizzDto) -> QuizzDto:
        """Create new quiz"""
        return None
    
    async def update(self, quizz_id: int, quizz: UpdateQuizzDto) -> QuizzDto:
        """Update quiz"""
        return None
    
    async def delete(self, quizz_id: int) -> bool:
        """Delete quiz"""
        return True

quizzService = QuizzService()