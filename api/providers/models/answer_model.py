from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from providers.models.mixins.timestamps_mixin import TimestampMixin
from providers.models.mixins.soft_delete_mixin import SoftDeleteMixin
from providers.postgree_provider import Base

class AnswerModel(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)