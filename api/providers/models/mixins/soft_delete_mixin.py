from sqlalchemy import Column, DateTime, func

class SoftDeleteMixin:
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)

    def soft_delete(self):
        self.deleted_at = func.now()    