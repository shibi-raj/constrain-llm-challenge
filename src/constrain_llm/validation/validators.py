from constrain_llm.models.schemas import Order
import re


class OrderValidator:

    def validate(self, order: Order, raw: str) -> str | None:
        if order.order_id not in raw:
            return "Order ID not found in source"

        if order.buyer not in raw:
            return "Buyer not found in source"

        if order.state not in raw:
            return "State not found in source"

        if f"{order.total:.2f}" not in raw:
            return "Total not found in source"

        return None


