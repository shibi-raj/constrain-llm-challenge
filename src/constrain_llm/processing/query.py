from constrain_llm.config.settings import LLM_PROVIDER, LLM_MODEL
from constrain_llm.llm.factory import create_llm
from constrain_llm.models.schemas import OrderQuery

SYSTEM_PROMPT = """
Convert the user's request into an OrderQuery.

Rules:
- Only populate fields explicitly specified by the user.
- Use null when a criterion is not specified.
- Do not infer or invent values.
- State must use the two-letter USPS abbreviation.
"""


class QueryProcessor:
    def __init__(self):
        self.llm = create_llm(
            provider=LLM_PROVIDER,
            model=LLM_MODEL,
        )

    def process(self, user_request: str) -> OrderQuery:
        structured_llm = self.llm.with_structured_output(OrderQuery)
        return structured_llm.invoke([
            ("system", SYSTEM_PROMPT),
            ("human", user_request),
        ])

    