from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    year: int
    genre: str
    pages: int
    available: bool
    cover_url: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    pages: Optional[int] = None
    available: Optional[bool] = None


class Book(BookBase):
    id: int

    model_config = {
        "from_attributes": True
    }
