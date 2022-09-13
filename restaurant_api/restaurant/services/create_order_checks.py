from django.db.models import QuerySet

from restaurant.models import Printer, Check
from restaurant.serializers import Order
from restaurant.exceptions.exceptions import PointHasNoPrinters, CheckAlreadyCreated


class PointOrderChecks:

    def create_checks_for_point(self, client_order: Order.data):
        """
        Creates checks for the all printers placed in some point and
        returns new records amount. Otherwise, if the order already
        exists, raises the exception.
        """
        self._check_order_is_new(client_order['id'])
        point_printers = self._get_all_printers_at_point(client_order['point_id'])
        new_checks_amount = self._create_new_checks_for_printers(client_order, point_printers)
        return new_checks_amount

    @staticmethod
    def _get_all_printers_at_point(point_id: int) -> QuerySet[Printer]:
        """
        Returns all printers placed at the point. Otherwise, raises
        the exception.
        """
        printers = Printer.objects.filter(point_id=point_id)
        if not printers.exists():
            raise PointHasNoPrinters
        return Printer.objects.filter(point_id=point_id)

    @staticmethod
    def _check_order_is_new(order_id: int) -> bool:
        """
        Returns `True` if order doesn't exist in the db.
        Otherwise, an error will be raised.
        """
        order = Check.objects.filter(order__id=order_id)
        if order.exists():
            raise CheckAlreadyCreated
        return True

    @staticmethod
    def _create_new_checks_for_printers(
            client_order: Order, point_printers: QuerySet[Printer]
    ) -> int:
        """
        Creates new checks for printers and returns amount of the new
        records.
        """
        new_checks = [
            Check(
                printer_id=printer,
                type=printer.check_type,
                order=client_order,
                status='new'
            ) for printer in point_printers
        ]
        return Check.objects.bulk_create(new_checks)
