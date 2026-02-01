from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from config.config import settings

from sqlalchemy import ForeignKey

engine = create_async_engine(settings.DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    
    email: Mapped[str | None] = mapped_column(unique=True, index=True, nullable=True)
    github_id: Mapped[int | None] = mapped_column(unique=True, index=True, nullable=True)

    tasks: Mapped[list["TaskORM"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    files = relationship("FileORM", back_populates="user", cascade="all, delete-orphan")

class TaskORM(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column (ForeignKey("users.id"), nullable=False)
    user: Mapped["UserORM"] = relationship(back_populates="tasks")

class FileORM(Base):
    __tablename__ = "Files"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    path: Mapped[str] = mapped_column(nullable=False)

    user = relationship("UserORM", back_populates="files")

async def setup_database():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
