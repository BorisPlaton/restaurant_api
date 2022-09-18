from django.db.models import QuerySet

from restaurant.models import Printer, Check
from restaurant.exceptions.exceptions import PointHasNoPrinters, CheckAlreadyCreated
from restaurant.services.commands.abstract import BaseCommand
from restaurant.services.commands.schemas import OrderData


class CreateOrderChecks(BaseCommand):
    """
    The command creates checks records in the database from user's order
    information.
    """

    def execute(self, client_order: OrderData):
        """
        Creates checks for the all printers placed in some point and
        returns all new `Check` instances. Otherwise, if the order already
        exists, raises the exception.
        """
        self._check_order_is_new(client_order['id'])
        point_printers = self._get_all_printers_at_point(client_order['point_id'])
        return self._create_new_checks_for_printers(client_order, point_printers)

    @staticmethod
    def _check_order_is_new(order_id: int) -> bool:
        """
        Returns `True` if order doesn't exist in the db.
        Otherwise, an error will be raised.

        The order doesn't exist in the db if the db doesn't have
        record whose `id` value of the `order` json-field is equal
        to the `order_id` parameter.
        """
        order = Check.objects.filter(order__id=order_id)
        if order.exists():
            raise CheckAlreadyCreated
        return True

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
    def _create_new_checks_for_printers(
            client_order: OrderData, point_printers: QuerySet[Printer]
    ) -> list[Check]:
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
