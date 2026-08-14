from constrain_llm.models.schemas import (
    Order,
    ParsedOrders,
    RawOrdersResponse,
    ValidationIssue,
)
from constrain_llm.validation.validators import OrderValidator
from constrain_llm.config.logging import get_logger
from constrain_llm.config.settings import LLM_PROVIDER, LLM_MODEL
from constrain_llm.llm.factory import create_llm


# import re
logger = get_logger(__name__)

SYSTEM_PROMPT = f"""
You are an information extraction system.

Extract values only from the provided source text.

For each field:
- Identify the field's value using the surrounding textual context.
- Prefer values explicitly associated with the field label.
- Do not infer, speculate, or use outside knowledge.
- Preserve the source value unless normalization is required by the schema.
- Do not add prefixes, labels, explanations, or conversational text to values.
- If multiple possible values exist, use the value most directly associated with the field.
- If a required value cannot be determined reliably, do not guess.
- Before returning the result, verify that every extracted value is supported by the source text.
"""

class OrderProcessor:

    def __init__(self, num_attempts: int = 2):
        self.llm = create_llm(
            provider=LLM_PROVIDER,
            model=LLM_MODEL,
        )

        self.structured_order_llm = (
            self.llm.with_structured_output(Order)
        )

        self.num_attempts = num_attempts

    def process(self, response: RawOrdersResponse) -> ParsedOrders:
        orders = []
        validation_issues = []

        for raw in response.raw_orders:
            try:
                order = self._parse_order(raw)
                orders.append(order)

            except ValueError as exc:
                validation_issues.append(
                    ValidationIssue(
                        raw_order=raw,
                        reason=str(exc),
                    )
                )

        return ParsedOrders(
            orders=orders,
            validation_issues=validation_issues,
        )

    def _parse_order(self, raw: str) -> Order:
        print("\n", raw)

        for attempt in range(self.num_attempts):
            try:
                order = self.structured_order_llm.invoke([
                    ("system", SYSTEM_PROMPT),
                    ("human", raw),
                ])

                print("llm order", order)

                reason = self.validator.validate(order, raw)

                if reason:
                    raise ValueError(reason)

                return order

            except Exception as e:
                if attempt == self.num_attempts - 1:
                    raise ValueError(
                        f"Order extraction failed after "
                        f"{self.num_attempts} attempts: {e}"
                    ) from e

                logger.warning(
                    f"Order extraction failed on attempt "
                    f"{attempt + 1}; retrying: {e}"
                )
                human_prompt = f"""
                    The previous extraction was invalid.
                    Validation failure: {e}
                    Re-examine the original order carefully. Correct the extraction.
                    The output must contain only values extracted from the original order.
                    Do not add prefixes, labels, or conversational text to field values.
                    For example, do not return "user:Order 1002" for order_id.
                    The field names are defined by the Order schema and must not be treated
                    as values.
                    Do not guess or invent values.
                    Original order: {raw}
                    """
        raise RuntimeError("Unexpected end of extraction loop")