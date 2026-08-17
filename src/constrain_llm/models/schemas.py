import re
import us
from pydantic import BaseModel, Field, field_validator, BeforeValidator
from typing import Annotated
from decimal import Decimal


def clean_city_string(v: str) -> str:
    """If the LLM passes 'Columbus, OH' as the city, strip the state suffix."""
    if isinstance(v, str) and "," in v:
        # Splits 'Columbus, OH' into ['Columbus', ' OH'] and takes the first part
        return v.split(",")[0].strip()
    return v

class Order(BaseModel):
    order_id: str = Field(
        description="The unique digits of the order identifier, excluding the word 'Order'.",
        examples=["1005", "1002"]
    )
    buyer: str = Field(
        description="The full first and last name of the customer.",
        examples=["Chris Myers"]
    )
    # city: str = Field(
    #     description="The clean name of the city only. Do not include the state.",
    #     examples=["Cincinnati", "Austin"]
    # )
    city: Annotated[str, BeforeValidator(clean_city_string)] = Field(
        description="The clean name of the city only. E.g., 'Columbus'"
    )

    state: str = Field(
        description="The 2-letter capitalized US state abbreviation only.",
        min_length=2,
        max_length=2,
        examples=["OH", "TX"]
    )
    total: float = Field(
        description="The total monetary cost of the order as a float. Strip out currency symbols like '$'.",
        gt=0.0,
        examples=[512.00, 156.55]
    )

    @field_validator("buyer")
    @classmethod
    def validate_buyer(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", value):
            raise ValueError("Buyer name contains invalid characters")
        return value

    @field_validator("state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        state = us.states.lookup(value)

        if state is None:
            raise ValueError(f"Invalid US state: {value}")

        return state.abbr

    @field_validator("total")
    @classmethod
    def validate_total(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Order total cannot be negative")
        return value


class RawOrdersResponse(BaseModel):
    status: str
    raw_orders: list[str]


class ValidationIssue(BaseModel):
    raw_order: str
    reason: str


class ParsedOrders(BaseModel):
    orders: list[Order]
    validation_issues: list[ValidationIssue] = []


class OrderQuery(BaseModel):
    state: str | None = None
    min_total: float | None = None
    max_total: float | None = None
    