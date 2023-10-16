from pydantic import BaseModel
# Pydantic models defined here

class UserBase(BaseModel):
    email: str

class User(UserBase):
    id: int
    is_active: bool
    first_name: str
    last_name: str

    class Config:
        orm_mode = True