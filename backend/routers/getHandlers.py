from fastapi import APIRouter, Depends
from repository import TaskRepository
from auth.dependencies import get_current_user

from schemas import Task

router = APIRouter(prefix="/tasks", tags=["Get Handlers"])

@router.get("", summary="Get all tasks")
async def get_tasks(current_user=Depends(get_current_user)) -> list[Task]:
    tasks_schemas = await TaskRepository.get_all_tasks(user_id=current_user.id)
    return tasks_schemas
