from providers.models.mixins.soft_delete_mixin import SoftDeleteMixin
from providers.models.mixins.timestamps_mixin import TimestampMixin
from sqlalchemy import Column, Integer, String, ForeignKey
from providers.postgree_provider import Base

class QuizzModel(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
