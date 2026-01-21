from fastapi import APIRouter
from repository import TaskRepository

from schemas import Task

router = APIRouter(prefix="/tasks", tags=["Get Handlers"])

@router.get("", summary="Get all tasks")
async def get_tasks() -> list[Task]:
    tasks_schemas = await TaskRepository.get_all_tasks()
    return tasks_schemas
