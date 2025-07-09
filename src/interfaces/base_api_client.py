from abc import ABC, abstractmethod
from httpx import Client
import logging
from typing import Optional, Dict, Any, Union


logger = logging.getLogger(__name__)


class BaseApiClient(ABC):

    timeout: float = 10.0

    def __init__(self):
        self._client = Client(timeout=self.timeout)

    @property
    @abstractmethod
    def base_url(self) -> str:
        pass

    def _full_url(self, endpoint: str) -> str:
        return endpoint if endpoint.startswith("http") else f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def _handle_request(self, method: str, url: str, **kwargs) -> Union[Dict[str, Any], bool]:
        logger.debug(f"{method.upper()} {url} | {kwargs}")
        response = self._client.request(method, url, **kwargs)
        response.raise_for_status()
        return True if method.lower() == "delete" else response.json()

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        return self._handle_request("get", self._full_url(endpoint), params=params, headers=headers)

    def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        return self._handle_request("post", self._full_url(endpoint), data=data, json=json, headers=headers)

    def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        return self._handle_request("put", self._full_url(endpoint), data=data, json=json, headers=headers)

    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> bool:
        result = self._handle_request("delete", self._full_url(endpoint), headers=headers)
        return bool(result)

    def close(self):
        self._client.close()
