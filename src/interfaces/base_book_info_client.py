# interfaces/base_book_info_client.py
from abc import ABC, abstractmethod
from typing import Optional


class BaseBookInfoClient(ABC):
    @abstractmethod
    def search_book(self, title: str, author: str) -> Optional[dict]:
        pass

    @abstractmethod
    def get_description(self, work_key: str) -> Optional[str]:
        pass

    @abstractmethod
    def get_rating(self, work_key: str) -> Optional[float]:
        pass

    @abstractmethod
    def get_cover_url(self, cover_id: int) -> Optional[str]:
        pass
