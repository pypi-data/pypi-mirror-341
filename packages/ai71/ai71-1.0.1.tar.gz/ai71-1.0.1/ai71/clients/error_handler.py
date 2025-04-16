import asyncio
from json.decoder import JSONDecodeError

import httpx
import httpx_sse
from httpx import ConnectTimeout, RequestError, TimeoutException
from pydantic import BaseModel

from .. import exceptions


class ClientErrorMixin:
    """A mixin for handling client-side errors in an SDK."""

    def handle_exception(self, e: Exception, *args):
        """Dispatches the appropriate handler based on the exception type."""
        if isinstance(e, httpx_sse._exceptions.SSEError):
            self.handle_sse_error(e, *args)
        elif isinstance(e, RequestError):
            self.handle_request_error(e)
        elif isinstance(e, TimeoutException):
            self.handle_timeout_error(e)
        elif isinstance(e, ConnectTimeout):
            self.handle_connect_timeout(e)
        elif isinstance(e, JSONDecodeError):
            self.handle_json_decode_error(e)
        elif isinstance(e, httpx.HTTPStatusError):
            self.handle_http_error(e)
        elif isinstance(e, KeyError):
            self.handle_key_error(e)
        elif isinstance(e, AttributeError):
            self.handle_attribute_error(e)
        elif isinstance(e, TypeError):
            self.handle_type_error(e)
        elif isinstance(e, asyncio.CancelledError):
            self.handle_cancelled_error(e)
        elif isinstance(e, ValueError):
            self.handle_value_error(e)
        else:
            self.handle_unexpected_error(e)

    def raise_api_error(self, string):
        raise exceptions.APIError(string)

    def handle_sse_error(
        self, e: httpx_sse._exceptions.SSEError, url: str, request: BaseModel
    ):
        self.raise_api_error(
            f"SSE operation failed for {url}: {e}, request : {request}"
        )

    def handle_request_error(self, e: RequestError):
        self.raise_api_error(f"Request error: {e}")

    def handle_timeout_error(self, e: TimeoutException):
        self.raise_api_error(f"Request timed out: {e}")

    def handle_connect_timeout(self, e: ConnectTimeout):
        self.raise_api_error(f"Connection timeout: {e}")

    def handle_json_decode_error(self, e: JSONDecodeError):
        self.raise_api_error(f"Invalid JSON response: {e}")

    def handle_http_error(self, e: httpx.HTTPStatusError):
        status_code = e.response.status_code
        self.raise_api_error(f"HTTP {status_code} error: {e.response.text}")

    def handle_key_error(self, e: KeyError):
        self.raise_api_error(f"Missing key: {e}")

    def handle_attribute_error(self, e: AttributeError):
        self.raise_api_error(f"Missing attribute: {e}")

    def handle_type_error(self, e: TypeError):
        self.raise_api_error(f"Type mismatch: {e}")

    def handle_cancelled_error(self, e: asyncio.CancelledError):
        self.raise_api_error("Operation was canceled.")

    def handle_value_error(self, e: ValueError):
        self.raise_api_error(f"Invalid value: {e}")

    def handle_unexpected_error(self, e: Exception):
        self.raise_api_error(f"Unexpected error: {e}")
