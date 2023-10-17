from pydantic import BaseModel

# Pydantic models defined here

class UserBase(BaseModel):
    email: str

class User(UserBase):
    is_active: bool
    first_name: str
    last_name: str

    class Config:
        from_attributes = True