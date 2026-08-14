from constrain_llm.models.schemas import Order, OrderQuery, ParsedOrders


class OrderFilter:
    def filter(
        self,
        orders: ParsedOrders,
        query: OrderQuery,
    ) -> list[Order]:

        return [
            order
            for order in orders.orders
            if (
                query.state is None
                or order.state == query.state
            )
            and (
                query.min_total is None
                or order.total >= query.min_total
            )
            and (
                query.max_total is None
                or order.total <= query.max_total
            )
        ]