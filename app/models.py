from pydantic import BaseModel, Field
from typing import List, Optional


class User(BaseModel):
    username: str
    password: str


class Note(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., description="Заголовок заметки")
    content: str = Field(..., description="Текст заметки")
    user_id: int = Field(..., description="ID пользователя")


class NoteCreator(BaseModel):
    title: str = Field(..., description="Заголовок новой заметки")
    content: str = Field(..., description="Текст новой заметки")


class NoteUpdater(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteOuter(Note):
    pass
