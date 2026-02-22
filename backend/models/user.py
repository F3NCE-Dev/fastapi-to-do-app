from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, intpk, created_at, updated_at
from config.config import settings

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    
    email: Mapped[str | None] = mapped_column(unique=True, index=True, nullable=True)
    github_id: Mapped[int | None] = mapped_column(unique=True, index=True, nullable=True)

    tasks: Mapped[list["TaskORM"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    picture_path: Mapped[str] = mapped_column(nullable=True, default=settings.DEFAULT_USER_PROFILE_PIC_PATH)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
