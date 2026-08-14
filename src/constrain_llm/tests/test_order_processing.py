from constrain_llm.api.customer_api import CustomerAPI
from constrain_llm.models.schemas import RawOrdersResponse
from constrain_llm.processing import OrderProcessor

from tests.data_mutations import (
    change_case,
    change_delimiters,
    rename_fields,
    reorder_fields,
    remove_field,
    add_unrelated_data,
    corrupt_total,
    corrupt_state,
    add_conflicting_state,
    add_hallucination_trap,
)


MUTATIONS = [
    ("original", lambda x: x),
    ("case", change_case),
    ("delimiters", change_delimiters),
    ("renamed fields", rename_fields),
    ("reordered fields", reorder_fields),
    ("missing buyer", lambda x: remove_field(x, "buyer")),
    ("unrelated data", add_unrelated_data),
    ("corrupt total", corrupt_total),
    ("corrupt state", corrupt_state),
    ("conflicting state", add_conflicting_state),
    ("hallucination trap", add_hallucination_trap),
]


def main():
    customer = CustomerAPI()
    raw_orders_response = customer.get_orders()

    # Use one order so mutation testing does not overwhelm the LLM.
    raw = raw_orders_response.raw_orders[0]

    processor = OrderProcessor()

    for name, mutation in MUTATIONS:
        print(f"\n{'=' * 60}")
        print(f"TEST: {name}")
        print(f"{'=' * 60}")

        mutated_raw = mutation(raw)

        print(f"Input:\n{mutated_raw}")

        test_response = RawOrdersResponse(
            status=raw_orders_response.status,
            raw_orders=[mutated_raw],
        )

        result = processor.process(test_response)

        print(f"Result:\n{result}")


if __name__ == "__main__":
    main()