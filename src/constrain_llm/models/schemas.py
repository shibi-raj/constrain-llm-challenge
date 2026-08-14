import re
import us
from pydantic import BaseModel, field_validator


class Order(BaseModel):
    order_id: str
    buyer: str
    state: str
    total: float

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
    