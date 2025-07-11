from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from ..core.config import settings
from ..infrastructure.clients.openlibrary_client.openlibrary_book_enricher import OpenLibraryBookEnricher
from ..infrastructure.clients.openlibrary_client.openlibrary_client import OpenLibraryClient
from ..infrastructure.repositories.db_repository.database import SessionLocal
from ..infrastructure.repositories.db_repository.db_repository import DBBookRepository
from ..infrastructure.repositories.file_repository import FileBookRepository
from ..infrastructure.repositories.jsonbin_repository import JsonBinBookRepository
from ..services.book_service import BookService


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache
def get_book_service(db: Session = Depends(get_db)) -> BookService:
    repo_type = settings.STORAGE_TYPE.lower()

    if repo_type == "file":
        repository = FileBookRepository()
    elif repo_type == "db":
        repository = DBBookRepository(db)
    elif repo_type == "jsonbin":
        repository = JsonBinBookRepository()
    else:
        raise ValueError(f"Unknown repository type: {repo_type}")

    enricher = OpenLibraryBookEnricher(OpenLibraryClient())
    return BookService(repository, enricher=enricher)
