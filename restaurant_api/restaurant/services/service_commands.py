from restaurant.serializers import Order
from restaurant.services.create_order_checks import CreateOrderChecks
from restaurant.services.generate_checks_pdf import GenerateChecksPdf


def create_new_order_and_generate_checks(client_order: Order) -> list[int]:
    """
    Creates new checks in the database and enqueues pdf files
    generation for them. Returns a list with models' `id` field.
    """
    new_checks = CreateOrderChecks().execute(client_order.data)
    checks_ids = [check.pk for check in new_checks]
    GenerateChecksPdf().execute(checks_ids)
    return checks_ids
