from pydantic import BaseModel

class TaskAdd(BaseModel):
    task: str
    status: bool

class Task(TaskAdd):
    id: int
