from typing import (
    AsyncIterator,
    Iterable,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)

import httpx
import pydantic

from ..clients import base_client

_ResponseT = TypeVar("_ResponseT", bound=pydantic.BaseModel)


class BaseResource:
    def __init__(self, client: base_client.BaseClient):
        self._client = client

    @overload
    def _post(
        self,
        url: str,
        model: pydantic.BaseModel,
        stream: Literal[False],
        cls: Type[_ResponseT],
    ) -> _ResponseT:
        ...

    @overload
    def _post(
        self,
        url: str,
        model: pydantic.BaseModel,
        stream: Literal[True],
        cls: Type[_ResponseT],
    ) -> Iterable[_ResponseT]:
        ...

    def _post(
        self, url: str, model: pydantic.BaseModel, stream: bool, cls: Type[_ResponseT]
    ) -> Union[_ResponseT, Iterable[_ResponseT]]:
        url_httpx = httpx.URL(url)

        if stream:
            return self._client.stream(url_httpx, model, cls)
        else:
            return self._client.post(url_httpx, model, cls)

    def _get(
        self, url: str, cls: Type[_ResponseT], params: Optional[dict] = {}
    ) -> _ResponseT:
        url_httpx = httpx.URL(url)

        return self._client.get(url=url_httpx, params=params, cls=cls)


class AsyncBaseResource:
    def __init__(self, client: base_client.AsyncBaseClient):
        self._client = client

    @overload
    async def _post(
        self,
        url: str,
        model: pydantic.BaseModel,
        stream: Literal[False],
        cls: Type[_ResponseT],
    ) -> _ResponseT:
        ...

    @overload
    async def _post(
        self,
        url: str,
        model: pydantic.BaseModel,
        stream: Literal[True],
        cls: Type[_ResponseT],
    ) -> AsyncIterator[_ResponseT]:
        ...

    async def _post(
        self, url: str, model: pydantic.BaseModel, stream: bool, cls: Type[_ResponseT]
    ) -> Union[_ResponseT, AsyncIterator[_ResponseT]]:
        url_httpx = httpx.URL(url)

        if stream:
            return self._client.stream(url_httpx, model, cls)
        else:
            return await self._client.post(url_httpx, model, cls)

    async def _get(
        self, url: str, cls: Type[_ResponseT], params: Optional[dict] = {}
    ) -> _ResponseT:
        url_httpx = httpx.URL(url)

        return await self._client.get(url=url_httpx, params=params, cls=cls)
