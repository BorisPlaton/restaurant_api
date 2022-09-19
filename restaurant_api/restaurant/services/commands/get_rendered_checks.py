from django.db.models import QuerySet

from restaurant.exceptions.exceptions import WrongPrinterApiKey
from restaurant.models import Printer, Check, CheckStatus
from restaurant.services.commands.abstract import BaseCommand


class GetRenderedChecks(BaseCommand):
    """
    Returns information about already rendered checks for
    specific printer.
    """

    def execute(self, printer_api_key: str):
        """
        Returns a QuerySet with `Check` instances which are already
        rendered for specific printer.
        """
        printer = self._get_printer(printer_api_key)
        return self._get_rendered_checks_for_printer(printer)

    @staticmethod
    def _get_rendered_checks_for_printer(printer: Printer) -> QuerySet[Check]:
        """
        Returns all rendered checks for printer
        """
        checks = Check.objects.filter(printer_id=printer, status=CheckStatus.RENDERED)
        return checks

    @staticmethod
    def _get_printer(printer_api_key: str):
        """
        Returns a `Printer` if it exists. Otherwise, exception raised.
        """
        printer = Printer.objects.filter(pk=printer_api_key)
        if not printer.exists():
            raise WrongPrinterApiKey
        return printer.first()
