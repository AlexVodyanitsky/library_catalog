import httpx
import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from .exceptions import BookNotFoundException, DataNotFoundException

logger = logging.getLogger(__name__)


async def book_not_found_handler(request: Request, exc: BookNotFoundException):
    logger.warning(f"[404] {exc.detail} - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def httpx_exception_handler(request: Request, exc: httpx.RequestError):
    logger.error(f"[External API] Request error: {exc} - {request.url}")
    return JSONResponse(
        status_code=502,
        content={"detail": "Ошибка подключения к внешнему API."}
    )


async def httpx_status_exception_handler(request: Request, exc: httpx.HTTPStatusError):
    logger.error(f"[External API] Status error: {exc.response.status_code} - {exc.response.text} - {request.url}")
    return JSONResponse(
        status_code=502,
        content={"detail": "Внешний API вернул ошибку."}
    )


async def data_not_found_handler(request: Request, exc: DataNotFoundException):
    logger.warning(f"[404 External] {exc.detail} - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
