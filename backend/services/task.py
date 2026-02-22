from fastapi import HTTPException

from models.task import TaskORM
from schemas.task import TaskAdd, Task

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class TaskRepository:
    @classmethod
    async def add_task(cls, data: TaskAdd, user_id: int, db: AsyncSession) -> int:
        task = TaskORM(**data.model_dump(), user_id=user_id)
        db.add(task)
        await db.commit()
        return task.id
        
    @classmethod
    async def delete_task(cls, id: int, user_id: int, db: AsyncSession) -> None:
        result = await db.execute(select(TaskORM).where(TaskORM.id == id, TaskORM.user_id == user_id))

        task = result.scalar_one_or_none()

        if task is None:
            raise HTTPException(status_code=404, detail="There is no task with that name")

        await db.delete(task)
        await db.commit()

    @classmethod
    async def set_task(cls, id: int, status: bool, user_id: int, db: AsyncSession) -> None:
        result = await db.execute(select(TaskORM).where(TaskORM.id == id, TaskORM.user_id == user_id))
        task = result.scalar_one_or_none()

        if task is None:
            raise HTTPException(status_code=404, detail="There is no task with that id")
        
        task.status = status

        await db.commit()

    @classmethod
    async def get_all_tasks(cls, user_id: int, db: AsyncSession) -> list[Task]:
        result = await db.execute(select(TaskORM).where(TaskORM.user_id == user_id))
        task_models = result.scalars().all()
        task_schemas = [Task.model_validate(task_model) for task_model in task_models]
        return task_schemas