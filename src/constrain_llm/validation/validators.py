from constrain_llm.models.schemas import Order
import re


class OrderValidator:
    """
    Hook for domain-specific business validation post-parsing.
    Pydantic handles structural type checking.
    This layer meamnt for future context-aware validation.
    """
    def validate(self, order: Order, raw: str) -> str | None:
        # Intentionally leaving open for downstream validation rules
        return None
