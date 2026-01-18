from fastapi import FastAPI, HTTPException, Depends
from schemas import *
import uvicorn

from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///tasks.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str]
    status: Mapped[bool]

@app.post("/setup_database", tags=["Post handlers"], summary="set a database")
async def setup_database():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"Success": True}

#GET
@app.get("/get tasks", tags=["get handlers"], summary="get all tasks")
async def GetTasks(session: SessionDep):
    query = select(Task)
    result = await session.execute(query)
    return result.scalars().all()

@app.get("/get a specific task", tags=["get handlers"], summary="get all tasks")
async def GetTask(task_id: int, session: SessionDep):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="There is no task with that name")

    return task

#POST
@app.post("/Create new task", tags=["Post handlers"], summary="Add a new task")
async def AddTask(data: TaskAdd, session: SessionDep):
    new_task = Task(
        task = data.task,
        status = data.status
    )
    session.add(new_task)
    await session.commit()
    return {"data successfully received": True}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
