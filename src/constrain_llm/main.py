from constrain_llm.api.customer_api import CustomerAPI
from constrain_llm.config.logging import get_logger
from constrain_llm.models.schemas import ParsedOrders, RawOrdersResponse
from constrain_llm.processing import (
    OrderFilter,
    OrderProcessor,
    QueryProcessor,
)
from constrain_llm.utils.time_utils import timed_call


logger = get_logger(__name__)


def get_user_request() -> str:
    return "Show me all orders where the buyer was located in Ohio and total value was over 500."


def main():
    # --- user input ---
    user_request = get_user_request()

    if not user_request:
        print("Please enter a request.")
        return

    # --- fetch customer orders ---
    customer = CustomerAPI()

    raw_orders_response: RawOrdersResponse = timed_call(
        customer.get_orders,
        "Fetch of all orders done in",
    )

    # --- parse raw orders into validated Order objects ---
    order_processor = OrderProcessor()

    parsed_orders: ParsedOrders = timed_call(
        order_processor.process,
        "Parsing orders took",
        raw_orders_response,
    )

    # --- convert natural-language request into OrderQuery ---
    query_processor = QueryProcessor()

    query = timed_call(
        query_processor.process,
        "Query processed in",
        user_request,
    )

    # --- filter orders according to OrderQuery ---
    order_filter = OrderFilter()

    results = timed_call(
        order_filter.filter,
        "Filtration time: ",
        parsed_orders,
        query,
    )

    # --- display results ---
    for result in results:
        print(result)


if __name__ == "__main__":
    main()