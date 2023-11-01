from typing import List
from pydantic import BaseModel
import enum

# Pydantic models defined here

class User(BaseModel):
    email: str
    password: str

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


class CollaborationPreference(enum.Enum):
    in_person = "In Person"
    online = "Online"
    no_preference = "No Preference"


class UserDetailUpdate(BaseModel):
    field: str # the column of the table you want to update
    data: str # new value of the column

class UserDetailCreate(BaseModel):
    first_name: str
    last_name: str
    title: str
    description: str
    preference: str
    address: str


class PersonalGenresUpload(BaseModel):
    id: List[int]

class PersonalInstrumentsUpload(BaseModel):
    id: List[int]