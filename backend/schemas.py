from pydantic import BaseModel, ConfigDict

class UserLogin(BaseModel):
    username: str
    password: str

class TaskAdd(BaseModel):
    task: str
    status: bool

class Task(TaskAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class Task_ID(BaseModel):
    success: bool
    task_id: int
