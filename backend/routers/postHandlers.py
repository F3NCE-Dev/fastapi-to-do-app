from fastapi import APIRouter

from repository import TaskRepository
from schemas import TaskAdd, Task_ID

router = APIRouter(tags=["Post Handlers"])

@router.post("/add", summary="Add a new task", response_model=Task_ID)
async def add_task(task: TaskAdd) -> Task_ID:
    task_id = await TaskRepository.add_task(task)
    return {"success": True, "task_id": task_id}

@router.post("/remove", summary="Remove a task")
async def delete_task(task_id: int):
    await TaskRepository.delete_task(task_id)
    return {"success": True, "detail": "Task's successfully deleted"}

@router.post("/set task status")
async def set_task_status(task_id: int, status: bool):
    await TaskRepository.set_task(task_id, status)
    return {"success": True, "detail": "Task's been succussfully updated"}
