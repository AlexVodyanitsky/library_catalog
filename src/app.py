import httpx
from fastapi import FastAPI
from .api.routes import router as book_router
from .core.logger import setup_logger
from .core.exception_handlers import (
    book_not_found_handler,
    data_not_found_handler,
    httpx_exception_handler,
    httpx_status_exception_handler
)

from .core.exceptions import BookNotFoundException, DataNotFoundException

setup_logger()

app = FastAPI(title="Library Catalog")
app.include_router(book_router)

app.add_exception_handler(BookNotFoundException, book_not_found_handler)
app.add_exception_handler(httpx.RequestError, httpx_exception_handler)
app.add_exception_handler(httpx.HTTPStatusError, httpx_status_exception_handler)
app.add_exception_handler(DataNotFoundException, data_not_found_handler)


@app.get("/")
def root():
    return {"message": "Library Catalog API"}
