from fastapi import APIRouter

from repository import TaskRepository
from dependencies import CurrentUser, DBSession
from schemas import Task, TaskAdd, StatusResponse, TaskAddResponse

router = APIRouter(tags=["Task Handlers"])

@router.get("/tasks", summary="Get all tasks")
async def get_tasks(current_user: CurrentUser, db: DBSession) -> list[Task]:
    tasks_schemas = await TaskRepository.get_all_tasks(user_id=current_user.id, db=db)
    return tasks_schemas

@router.post("/add", summary="Add a new task", response_model=TaskAddResponse)
async def add_task(task: TaskAdd, current_user: CurrentUser, db: DBSession):
    task_id = await TaskRepository.add_task(task, current_user.id, db)
    return {"success": True, "task_id": task_id}

@router.delete("/remove/{task_id}", summary="Remove a task", response_model=StatusResponse)
async def delete_task(task_id: int, current_user: CurrentUser, db: DBSession):
    await TaskRepository.delete_task(task_id, current_user.id, db)
    return {"success": True, "detail": "Task's successfully deleted"}

@router.patch("/set-task-status/{task_id}", response_model=StatusResponse)
async def set_task_status(task_id: int, status: bool, current_user: CurrentUser, db: DBSession):
    await TaskRepository.set_task(task_id, status, current_user.id, db)
    return {"success": True, "detail": "Task's been successfully updated"}
