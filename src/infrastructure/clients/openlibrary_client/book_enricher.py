import logging
from typing import Optional, Dict

from .openlibrary_client import OpenLibraryClient


logger = logging.getLogger(__name__)


class BookEnricher:
    def __init__(self, client: OpenLibraryClient):
        self.client = client

    def enrich(self, title: str, author: str) -> Dict[str, Optional[str | float]]:
        logger.info(f"Ищем инфу по книге: {title} by {author}")

        book_data = self.client.search_book(title, author)
        if not book_data:
            logger.warning("Данные книги не найдены в OpenLibrary.")
            return {}

        work_key = book_data.get("key")
        cover_id = book_data.get("cover_i")

        description = self.client.get_description(work_key)
        rating = self.client.get_rating(work_key)
        cover_url = self.client.get_cover_url(cover_id)

        enriched_data = {
            "description": description[:500] if description else None,
            "rating": rating,
            "cover_url": cover_url,
        }

        logger.debug(f"Нашли инфу: {enriched_data}")
        return enriched_data
