import logging
from typing import List, Optional

from ..core.exceptions import BookNotFoundException, DataNotFoundException
from ..models.schemas import Book, BookCreate, BookUpdate
from ..interfaces.base_repository import BaseBookRepository
from ..infrastructure.clients.openlibrary_client.openlibrary_book_enricher import OpenLibraryBookEnricher


logger = logging.getLogger(__name__)


class BookService:
    def __init__(self, repository: BaseBookRepository, enricher: Optional[OpenLibraryBookEnricher] = None):
        self.repository = repository
        self.enricher = enricher

    def get_books(self, **filters) -> List[Book]:
        books = self.repository.get_books(**filters)
        logger.info(f"Найдено {len(books)} книг")
        return books

    def get_book(self, book_id: int) -> Optional[Book]:
        logger.debug(f"Получение книги ID={book_id}")
        book = self.repository.get_book(book_id)
        if book:
            logger.info(f"Книга найдена: {book.title} автор {book.author}")
        else:
            raise BookNotFoundException(book_id)
        return book

    def add_book(self, book_create: BookCreate) -> Book:
        logger.info(f"Добавление новой книги: {book_create.title} автор: {book_create.author}")
        if self.enricher:
            enriched = self.enricher.enrich(book_create.title, book_create.author)
            if enriched:
                book_create.cover_url = enriched.get("cover_url")
                book_create.description = enriched.get("description")
                book_create.rating = enriched.get("rating")
            else:
                raise DataNotFoundException(message="Информация не найдена")
        book = self.repository.add_book(book_create)
        logger.info(f"Книга {book.title} добавлена. Автор: {book.author}")
        return book

    def update_book(self, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        logger.info(f"Обновление книги id={book_id} данными: {book_update}")
        book = self.repository.update_book(book_id, book_update)
        if book:
            logger.info(f"Книга с id={book_id} обновлена")
        else:
            raise BookNotFoundException(book_id)
        return book

    def delete_book(self, book_id: int) -> bool:
        logger.info(f"Удаление книги с id={book_id}")
        success = self.repository.delete_book(book_id)
        if success:
            logger.info(f"Книга с id={book_id} удалена")
        else:
            raise BookNotFoundException(book_id)
        return success
