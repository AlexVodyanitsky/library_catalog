from fastapi import HTTPException, status


class BookNotFoundException(HTTPException):
    def __init__(self, book_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с id {book_id} не найдена."
        )


class DataNotFoundException(HTTPException):
    def __init__(self, message: str = "Информация не найдена во внешнем источнике"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )
