from providers.models.mixins.soft_delete_mixin import SoftDeleteMixin
from providers.models.mixins.timestamps_mixin import TimestampMixin
from sqlalchemy import Column, Integer, String
from providers.postgree_provider import Base
import bcrypt

class UserModel(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, nullable=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def set_password(self, password: str) -> None:
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
