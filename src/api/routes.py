from fastapi import APIRouter, Depends
from typing import List, Optional

from ..dependencies.dependencies import get_book_service
from ..models.schemas import Book, BookCreate, BookUpdate
from ..services.book_service import BookService


router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[Book])
def get_books(
    genre: Optional[str] = None,
    available: Optional[bool] = None,
    service: BookService = Depends(get_book_service),
):
    return service.get_books(genre=genre, available=available)


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, service: BookService = Depends(get_book_service)):
    book = service.get_book(book_id)
    return book


@router.post("/", response_model=Book)
def add_book(book_data: BookCreate, service: BookService = Depends(get_book_service)):
    return service.add_book(book_data)


@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book_data: BookUpdate, service: BookService = Depends(get_book_service)):
    book = service.update_book(book_id, book_data)
    return book


@router.delete("/{book_id}")
def delete_book(book_id: int, service: BookService = Depends(get_book_service)):
    success = service.delete_book(book_id)
    return {"deleted": success}
