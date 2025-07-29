from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None

class BookRead(BookCreate):
    id: int

    class Config:
        orm_mode = True
