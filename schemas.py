from pydantic import BaseModel
from datetime import datetime

class NoteBase(BaseModel):
    title: str
    description: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    owner_id: int

    class config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    notes: list[Note] = []

    class config:
        orm_mode = True