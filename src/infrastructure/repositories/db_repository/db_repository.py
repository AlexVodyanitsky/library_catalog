from typing import Optional

from sqlalchemy.orm import Session

from ....interfaces.base_repository import BaseBookRepository
from ....models.models import BookModel
from ....models.schemas import Book, BookCreate, BookUpdate


class DBBookRepository(BaseBookRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_books(self, genre: str = None, available: bool = None):
        query = self.db.query(BookModel)
        if genre:
            query = query.filter(BookModel.genre == genre)
        if available is not None:
            query = query.filter(BookModel.available == available)
        books = query.all()
        return [Book.from_orm(book) for book in books]

    def get_book(self, book_id: int) -> Optional[Book]:
        book = self.db.query(BookModel).filter(BookModel.id == book_id).first()
        return Book.from_orm(book) if book else None

    def add_book(self, book_data: BookCreate) -> Book:
        book = BookModel(**book_data.dict())
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return Book.from_orm(book)

    def update_book(self, book_id: int, book_data: BookUpdate) -> Optional[Book]:
        book = self.db.query(BookModel).filter(BookModel.id == book_id).first()
        if not book:
            return None
        for field, value in book_data.dict(exclude_unset=True).items():
            setattr(book, field, value)
        self.db.commit()
        self.db.refresh(book)
        return Book.from_orm(book)

    def delete_book(self, book_id: int) -> bool:
        book = self.db.query(BookModel).filter(BookModel.id == book_id).first()
        if not book:
            return False
        self.db.delete(book)
        self.db.commit()
        return True
