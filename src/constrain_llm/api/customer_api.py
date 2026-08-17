from typing import Any
import requests
from constrain_llm.models.schemas import RawOrdersResponse


class CustomerAPI:
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url.rstrip("/")

    def get_orders(self, limit: int | None = None) -> RawOrdersResponse:
        params = {"limit": limit} if limit is not None else {}

        response = requests.get(
            f"{self.base_url}/api/orders",
            params=params,
            timeout=10,
        )
        response.raise_for_status()

        return RawOrdersResponse(**response.json())

    def get_order(self, order_id: str) -> str:
        response = requests.get(
            f"{self.base_url}/api/order/{order_id}",
            timeout=10,
        )
        response.raise_for_status()

        data: dict[str, Any] = response.json()
        return data["raw_order"]