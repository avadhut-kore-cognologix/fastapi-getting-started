from pydantic import BaseModel

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

class User(UserBase):
    id: int
    is_active: bool
    notes: list[Note] = []

    class config:
        orm_mode = True