from pydantic import BaseModel, Field, ConfigDict

class TaskAdd(BaseModel):
    task: str = Field(default="task", min_length=1, max_length=255)
    status: bool = False

class Task(TaskAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
