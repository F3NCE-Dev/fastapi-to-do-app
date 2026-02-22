from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database import Base, intpk, created_at, updated_at

class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[intpk]
    task: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    user: Mapped["UserORM"] = relationship(back_populates="tasks")

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
