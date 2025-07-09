from logging import getLogger
from typing import List

from ...models.schemas import Book
from ...core.config import settings
from ...interfaces.base_api_client import BaseApiClient

logger = getLogger(__name__)


class JsonBinClient(BaseApiClient):
    def __init__(self):
        super().__init__()
        self.bin_id = settings.JSONBIN_BIN_ID
        self.secret_key = settings.JSONBIN_API_KEY

    @property
    def base_url(self) -> str:
        return "https://api.jsonbin.io/v3"

    def _auth_headers(self) -> dict:
        return {
            "X-Master-Key": self.secret_key,
            "Content-Type": "application/json",
        }

    def get_all_books(self) -> List[Book]:
        endpoint = f"/b/{self.bin_id}/latest"
        response = self.get(endpoint, headers=self._auth_headers())

        raw_books = response.get("record")
        if isinstance(raw_books, dict) and "record" in raw_books:
            raw_books = raw_books["record"]

        if isinstance(raw_books, list):
            return [Book(**b) for b in raw_books]

        return []

    def save_books(self, books: List[dict]) -> bool:
        endpoint = f"/b/{self.bin_id}"
        payload = {"record": books}
        result = self.put(endpoint, json=payload, headers=self._auth_headers())
        return result is not None
