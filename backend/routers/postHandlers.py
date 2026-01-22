from fastapi import APIRouter, Depends

from repository import TaskRepository
from schemas import TaskAdd, Task_ID
from auth.dependencies import get_current_user
from database import UserORM

router = APIRouter(tags=["Post Handlers"])

@router.post("/add", summary="Add a new task", response_model=Task_ID)
async def add_task(task: TaskAdd, current_user: UserORM = Depends(get_current_user)) -> Task_ID:
    task_id = await TaskRepository.add_task(task, current_user.id)
    return {"success": True, "task_id": task_id}

@router.post("/remove", summary="Remove a task")
async def delete_task(task_id: int, current_user: UserORM = Depends(get_current_user)):
    await TaskRepository.delete_task(task_id, current_user.id)
    return {"success": True, "detail": "Task's successfully deleted"}

@router.post("/set task status")
async def set_task_status(task_id: int, status: bool, current_user: UserORM = Depends(get_current_user)):
    await TaskRepository.set_task(task_id, status, current_user.id)
    return {"success": True, "detail": "Task's been succussfully updated"}
