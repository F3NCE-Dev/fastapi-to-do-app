from pydantic import BaseModel, Field, constr

UsernameStr = constr(min_length=1, max_length=25, pattern=r"^[a-zA-Z0-9_-]+$")

class UserAuthData(BaseModel):
    username: str = UsernameStr
    password: str = Field(min_length=5, max_length=25)

class UserNewName(BaseModel):
    new_name: str = UsernameStr

class UserID(BaseModel):
    id: int
    username: str
