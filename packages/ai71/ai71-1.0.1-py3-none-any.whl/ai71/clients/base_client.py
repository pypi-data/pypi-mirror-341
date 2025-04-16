from typing import AsyncIterator, Iterable, Mapping, Optional, Type, TypeVar

import httpx
import httpx_sse
import pydantic

_ResponseT = TypeVar("_ResponseT", bound=pydantic.BaseModel)


class BaseClient:
    def __init__(
        self,
        headers: Mapping[str, str],
        base_url: httpx.URL,
        timeout: httpx.Timeout,
    ) -> None:
        self._client = httpx.Client(
            headers=headers,
            base_url=base_url,
            timeout=timeout,
        )

    def post(
        self, url: httpx.URL, request: pydantic.BaseModel, cls: Type[_ResponseT]
    ) -> _ResponseT:
        try:
            response = self._client.post(
                url,
                json=request.model_dump(),
            )
        except Exception as e:
            self.handle_exception(e, url, request)

        if response.status_code != httpx.codes.OK:
            self.handle_exception(
                httpx.HTTPStatusError(
                    f"Request failed with status {response.status_code}",
                    request=response.request,
                    response=response,
                ),
                url,
                request,
            )

        return cls.model_validate(response.json())

    def get(
        self, url: str, cls: Type[_ResponseT], params: Optional[dict] = {}
    ) -> _ResponseT:
        try:
            response = self._client.get(url, params=params)
        except Exception as e:
            self.handle_exception(e, url)

        if response.status_code != httpx.codes.OK:
            self.handle_exception(
                httpx.HTTPStatusError(
                    f"Request failed with status {response.status_code}",
                    request=response.request,
                    response=response,
                ),
                url,
            )

        return cls.model_validate(response.json())

    def stream(
        self, url: httpx.URL, request: pydantic.BaseModel, cls: Type[_ResponseT]
    ) -> Iterable[_ResponseT]:
        try:
            with httpx_sse.connect_sse(
                self._client,
                method="POST",
                url=str(url),
                json=request.model_dump(),
            ) as event_source:
                for response in event_source.iter_sse():
                    yield cls.model_validate(response.json())

        except httpx_sse._exceptions.SSEError as e:
            self._handle_sse_error(e, url, request)
        except Exception as e:
            self.handle_exception(e, url, request)

    def _handle_sse_error(
        self,
        e: httpx_sse._exceptions.SSEError,
        url: httpx.URL,
        request: pydantic.BaseModel,
    ):
        if "application/json" in str(e):
            # The server might be returning JSON instead of an SSE stream.
            # To debug this, we make a regular HTTP request to see the actual response.
            response = self._client.post(url=str(url), json=request.model_dump())

            try:
                error_info = (
                    response.json()
                    if response.headers.get("Content-Type") == "application/json"
                    else {}
                )
                detail = error_info.get("detail", "No detail provided.")
            except ValueError:
                detail = "Failed to parse JSON error response."

            self.handle_exception(
                Exception(
                    f"Fallback error message from sse exception, Status: {response.status_code}, Detail: {detail}, Response: {response.text}"
                ),
                url,
                request,
            )
        else:
            self.handle_exception(e, url, request)


class AsyncBaseClient:
    def __init__(
        self,
        headers: Mapping[str, str],
        base_url: httpx.URL,
        timeout: httpx.Timeout,
    ) -> None:
        self._client = httpx.AsyncClient(
            headers=headers,
            base_url=base_url,
            timeout=timeout,
        )

    async def post(
        self, url: httpx.URL, request: pydantic.BaseModel, cls: Type[_ResponseT]
    ) -> _ResponseT:
        try:
            response = await self._client.post(
                url,
                json=request.model_dump(),
            )
        except Exception as e:
            self.handle_exception(e, url, request)

        if response.status_code != httpx.codes.OK:
            self.handle_exception(
                httpx.HTTPStatusError(
                    f"Request failed with status {response.status_code}",
                    request=response.request,
                    response=response,
                ),
                url,
                request,
            )
        return cls.model_validate(response.json())

    async def stream(
        self, url: httpx.URL, request: pydantic.BaseModel, cls: Type[_ResponseT]
    ) -> AsyncIterator[_ResponseT]:
        try:
            async with httpx_sse.aconnect_sse(
                self._client,
                method="POST",
                url=str(url),
                json=request.model_dump(),
            ) as event_source:
                async for response in event_source.aiter_sse():
                    yield cls.model_validate(response.json())
        except httpx_sse._exceptions.SSEError as e:
            await self._handle_sse_error(e, url, request)
        except Exception as e:
            self.handle_exception(e, url, request)

    async def _handle_sse_error(
        self,
        e: httpx_sse._exceptions.SSEError,
        url: httpx.URL,
        request: pydantic.BaseModel,
    ):
        if "application/json" in str(e):
            # The server might be returning JSON instead of an SSE stream.
            # To debug this, we make a regular HTTP request to see the actual response.
            response = await self._client.post(url=str(url), json=request.model_dump())

            try:
                error_info = (
                    response.json()
                    if response.headers.get("Content-Type") == "application/json"
                    else {}
                )
                detail = error_info.get("detail", "No detail provided.")
            except ValueError:
                detail = "Failed to parse JSON error response."

            self.handle_exception(
                Exception(
                    f"Fallback error message from sse exception, Status: {response.status_code}, Detail: {detail}, Response: {response.text}"
                ),
                url,
                request,
            )
        else:
            self.handle_exception(e, url, request)

    async def get(
        self, url: str, cls: Type[_ResponseT], params: Optional[dict] = {}
    ) -> _ResponseT:
        try:
            response = await self._client.get(url, params=params)
        except Exception as e:
            self.handle_exception(e, url)

        if response.status_code != httpx.codes.OK:
            self.handle_exception(
                httpx.HTTPStatusError(
                    f"Request failed with status {response.status_code}",
                    request=response.request,
                    response=response,
                ),
                url,
            )

        return cls.model_validate(response.json())
