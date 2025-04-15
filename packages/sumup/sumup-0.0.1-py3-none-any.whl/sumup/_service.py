import httpx


class BaseClient:
    @staticmethod
    def version():
        return "0.0.1"  # x-release-please-version


class Service(BaseClient):
    _client: httpx.Client

    def __init__(self, client: httpx.Client) -> None:
        self._client = client


class AsyncService(BaseClient):
    _client: httpx.AsyncClient

    def __init__(self, client: httpx.Client) -> None:
        self._client = client
