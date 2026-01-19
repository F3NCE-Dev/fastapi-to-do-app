from fastapi import APIRouter, Depends

from repository import TaskRepository
from schemas import TaskAdd, Task_ID, Task_Add_Status

from typing import Annotated

router = APIRouter(tags=["Post Handlers"])

@router.post("/add", summary="Add a new task")
async def add_task(task: Annotated[TaskAdd, Depends()]) -> Task_ID:
    task_id = await TaskRepository.add_task(task)
    return {"ok": True, "task_id": task_id}

@router.post("/remove", summary="Remove a task")
async def delete_task(task_id: int) -> Task_Add_Status:
    deleted_task = await TaskRepository.delete_task(task_id)
    return deleted_task
