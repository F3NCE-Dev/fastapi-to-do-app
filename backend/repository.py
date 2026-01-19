from database import new_session, TaskORM
from schemas import TaskAdd, Task
from fastapi import HTTPException

from sqlalchemy import select

class TaskRepository:
    @classmethod
    async def add_task(cls, data: TaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskORM(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id
        
    @classmethod
    async def delete_task(cls, id: int) -> None:
        async with new_session() as session:
            result = await session.execute(
            select(TaskORM).where(TaskORM.id == id)
        )
        task = result.scalar_one_or_none()

        if task is None:
            raise HTTPException(status_code=404, detail="There is no task with that name")

        await session.delete(task)
        await session.commit()

    @classmethod
    async def get_all_tasks(cls) -> list[Task]:
        async with new_session() as session:
            query = select(TaskORM)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [Task.model_validate(task_model) for task_model in task_models]
            return task_schemas
