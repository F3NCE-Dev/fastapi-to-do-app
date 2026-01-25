from pydantic import BaseModel, ConfigDict, Field

class UserLogin(BaseModel):
    username: str = Field(default="username", min_length=1, max_length=25, pattern=r"^[a-zA-Z0-9_-]+$")
    password: str = Field(default=12345, min_length=5, max_length=25)

class User_ID(BaseModel):
    id: int
    username: str

class TaskAdd(BaseModel):
    task: str = Field(min_length=1, max_length=255)
    status: bool

class Task(TaskAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class Task_ID(BaseModel):
    success: bool
    task_id: int
