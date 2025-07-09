from abc import ABC, abstractmethod
from typing import List, Optional

from ..models.schemas import Book, BookCreate, BookUpdate


class BaseBookRepository(ABC):
    @abstractmethod
    def get_books(self, genre: Optional[str] = None, available: Optional[bool] = None) -> List[Book]:
        pass

    @abstractmethod
    def get_book(self, book_id: int) -> Optional[Book]:
        pass

    @abstractmethod
    def add_book(self, book_data: BookCreate) -> Book:
        pass

    @abstractmethod
    def update_book(self, book_id: int, book_data: BookUpdate) -> Optional[Book]:
        pass

    @abstractmethod
    def delete_book(self, book_id: int) -> bool:
        pass
