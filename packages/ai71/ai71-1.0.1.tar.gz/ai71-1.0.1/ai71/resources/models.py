from ..clients import base_client
from ..types.models import ModelsList
from . import base_resource


class Models(base_resource.BaseResource):
    def __init__(self, client: base_client.BaseClient) -> None:
        super().__init__(client)

    def list(self) -> ModelsList:
        return self._get("/models", params={}, cls=ModelsList)


class AsyncModels(base_resource.AsyncBaseResource):
    def __init__(self, client: base_client.AsyncBaseClient) -> None:
        super().__init__(client)

    async def list(self) -> ModelsList:
        return await self._get("/models", params={}, cls=ModelsList)
