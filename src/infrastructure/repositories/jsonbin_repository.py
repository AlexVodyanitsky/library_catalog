from typing import List, Optional

from ..clients.jsonbin_client import JsonBinClient
from ...interfaces.base_repository import BaseBookRepository
from ...models.schemas import BookCreate, BookUpdate, Book


class JsonBinBookRepository(BaseBookRepository):
    def __init__(self):
        self.client = JsonBinClient()

    def _load_data(self) -> List[Book]:
        return self.client.get_all_books()

    def _save_data(self, books: List[Book]) -> None:
        json_data = [book.dict() for book in books]
        self.client.save_books(json_data)

    @staticmethod
    def _get_next_id(books: List[Book]) -> int:
        if not books:
            return 1
        return max(book.id for book in books) + 1

    def get_books(self, genre: Optional[str] = None, available: Optional[bool] = None) -> List[Book]:
        books = self._load_data()
        if genre:
            books = [b for b in books if b.genre == genre]
        if available is not None:
            books = [b for b in books if b.available == available]
        return books

    def get_book(self, book_id: int) -> Optional[Book]:
        books = self._load_data()
        return next((b for b in books if b.id == book_id), None)

    def add_book(self, book_create: BookCreate) -> Book:
        books = self._load_data()
        new_id = self._get_next_id(books)
        new_book = Book(id=new_id, **book_create.dict())
        books.append(new_book)
        self._save_data(books)
        return new_book

    def update_book(self, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        books = self._load_data()
        for idx, book in enumerate(books):
            if book.id == book_id:
                updated_data = book.model_copy(update=book_update.dict(exclude_unset=True))
                books[idx] = updated_data
                self._save_data(books)
                return updated_data
        return None

    def delete_book(self, book_id: int) -> bool:
        books = self._load_data()
        filtered_books = [b for b in books if b.id != book_id]
        if len(books) == len(filtered_books):
            return False
        self._save_data(filtered_books)
        return True
