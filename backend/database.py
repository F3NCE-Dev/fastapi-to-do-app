from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column

from config.config import settings

from sqlalchemy import DateTime, func
from datetime import datetime
from typing import Annotated

engine = create_async_engine(settings.DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())]

class Base(DeclarativeBase):
    pass

async def setup_database():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
