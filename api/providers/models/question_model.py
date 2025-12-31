from sqlalchemy import Column, Integer, String, ForeignKey
from providers.models.mixins.soft_delete_mixin import SoftDeleteMixin
from providers.models.mixins.timestamps_mixin import TimestampMixin
from providers.postgree_provider import Base

class QuestionModel(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quizz_id = Column(Integer, ForeignKey("quizzes.id"))
    question_text = Column(String, nullable=False)