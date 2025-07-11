import logging
from typing import Optional, Dict, Any
from urllib.parse import urlencode

from ....interfaces.base_api_client import BaseApiClient
from ....interfaces.base_book_info_client import BaseBookInfoClient

logger = logging.getLogger(__name__)


class OpenLibraryClient(BaseApiClient, BaseBookInfoClient):
    @property
    def base_url(self) -> str:
        return "https://openlibrary.org"

    def search_book(self, title: str, author: str) -> Optional[Dict[str, Any]]:
        query = urlencode({"title": title, "author": author})
        response = self.get(f"/search.json?{query}")
        if response and response.get("docs"):
            logger.info(f"Найдена книга: {response['docs'][0].get('title')}")
            return response["docs"][0]
        logger.warning(f"Книга не найдена: {title} by {author}")
        return None

    def get_description(self, work_key: Optional[str]) -> Optional[str]:
        if not work_key:
            return None
        response = self.get(f"{work_key}.json")
        if not response:
            return None
        description = response.get("description")
        if isinstance(description, dict):
            return description.get("value")
        elif isinstance(description, str):
            return description
        return None

    def get_rating(self, work_key: Optional[str]) -> Optional[float]:
        if not work_key:
            return None
        response = self.get(f"{work_key}/ratings.json")
        if not response:
            return None
        rating = response.get("summary", {}).get("average")
        return float(rating) if rating is not None else None

    @staticmethod
    def get_cover_url(cover_id: Optional[int]) -> Optional[str]:
        if not cover_id:
            return None
        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
