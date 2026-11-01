# Test fixture (own example): handler with missing object-level authorization.
from db import fetch_order


def get_order(request, order_id):
    order = fetch_order(order_id)
    return {"id": order.id, "total": order.total, "customer": order.customer_id}
