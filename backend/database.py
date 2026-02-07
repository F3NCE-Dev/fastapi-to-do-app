from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from config.config import settings

from sqlalchemy import ForeignKey, DateTime, func
from datetime import datetime
from typing import Annotated

engine = create_async_engine(settings.DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

intpk = Annotated[int, mapped_column(primary_key=True)]

created_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())]

class Base(DeclarativeBase):
    pass

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    
    email: Mapped[str | None] = mapped_column(unique=True, index=True, nullable=True)
    github_id: Mapped[int | None] = mapped_column(unique=True, index=True, nullable=True)

    tasks: Mapped[list["TaskORM"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    files: Mapped[list["FileORM"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[intpk]
    task: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    user: Mapped["UserORM"] = relationship(back_populates="tasks")

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class FileORM(Base):
    __tablename__ = "files"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    path: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["UserORM"] = relationship(back_populates="files")

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

async def setup_database():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
