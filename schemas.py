from pydantic import BaseModel, ConfigDict

class TaskAdd(BaseModel):
    task: str
    status: bool

class Task(TaskAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class Task_ID(BaseModel):
    ok: bool
    task_id: int

class Task_Add_Status(BaseModel):
    ok: bool
    detail: str