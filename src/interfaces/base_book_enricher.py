from abc import abstractmethod, ABC
from typing import Dict, Optional, Union

from .base_api_client import BaseApiClient


class BaseBookEnricher(ABC):

    @abstractmethod
    def enrich(self, title: str, author: str) -> Dict[str, Optional[Union[str, float]]]:
        pass
