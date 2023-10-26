from pydantic import BaseModel

# Pydantic models defined here

class UserBase(BaseModel):
    email: str
    password: str

class User(UserBase):
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class Genre(BaseModel):
    name: str

    class Config:
        from_attributes = True

class Instrument(BaseModel):
    name: str

    class Config:
        from_attributes = True