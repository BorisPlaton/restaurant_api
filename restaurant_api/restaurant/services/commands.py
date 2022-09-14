from restaurant.serializers import Order
from restaurant.services.create_order_checks import CreateOrderChecks


def create_new_order_and_generate_checks(client_order: Order):
    """
    Creates new checks in the database and enqueues pdf files
    generation for them.
    """
    new_checks = CreateOrderChecks().execute(client_order.data)
