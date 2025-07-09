import json
from pathlib import Path
from typing import List, Optional

from ...interfaces.base_repository import BaseBookRepository
from ...models.schemas import Book, BookCreate, BookUpdate


class FileBookRepository(BaseBookRepository):
    def __init__(self, file_path: str = "books.json"):
        self.file_path = Path(file_path)
        self.file_path.touch(exist_ok=True)
        if self.file_path.read_text().strip() == "":
            self._write_data([])

    def _read_data(self) -> List[dict]:
        with self.file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_data(self, data: List[dict]) -> None:
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_books(self, genre: Optional[str] = None, available: Optional[bool] = None) -> List[Book]:
        books_data = self._read_data()
        books = [Book(**b) for b in books_data]
        if genre:
            books = [b for b in books if b.genre == genre]
        if available is not None:
            books = [b for b in books if b.available == available]
        return books

    def get_book(self, book_id: int) -> Optional[Book]:
        for b in self._read_data():
            if b["id"] == book_id:
                return Book(**b)
        return None

    def add_book(self, book_data: BookCreate) -> Book:
        books = self._read_data()
        new_id = max([b["id"] for b in books], default=0) + 1
        book_dict = book_data.dict()
        book_dict["id"] = new_id
        books.append(book_dict)
        self._write_data(books)
        return Book(**book_dict)

    def update_book(self, book_id: int, book_data: BookUpdate) -> Optional[Book]:
        books = self._read_data()
        for i, b in enumerate(books):
            if b["id"] == book_id:
                updated = b | book_data.dict(exclude_unset=True)
                books[i] = updated
                self._write_data(books)
                return Book(**updated)
        return None

    def delete_book(self, book_id: int) -> bool:
        books = self._read_data()
        new_books = [b for b in books if b["id"] != book_id]
        if len(books) == len(new_books):
            return False
        self._write_data(new_books)
        return True
