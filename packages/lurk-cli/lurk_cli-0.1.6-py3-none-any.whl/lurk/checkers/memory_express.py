from lurk.http_client import HttpClient
from lurk.checkers.checker import Checker
from lurk.config import SearchFilters
from lurk.models import Product


class MemoryExpressChecker(Checker):
    base_url = "https://www.memoryexpress.com"

    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client.set_base_url(self.base_url)

    async def get_products(
        self, search: str, filters: SearchFilters | None = None
    ) -> list[Product]:
        resp = await self.http_client.get(
            "/search",
            params={"q": search},
            expect_json=True,
        )
        return []
