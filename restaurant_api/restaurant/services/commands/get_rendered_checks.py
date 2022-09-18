from restaurant.models import Printer
from restaurant.services.commands.abstract import BaseCommand


class GetRenderedChecks(BaseCommand):
    """
    Returns information about already rendered checks for
    specific printer.
    """

    def execute(self, printer_api_key: str):
        """
        Returns a list of `Check` models' `id` fields which is
        already rendered for specific printer.
        """
        printer = self._get_printer(printer_api_key)

    def _get_rendered_checks_for_printer(self, printer: Printer):
        """
        Returns all rendered checks for printer
        """

    @staticmethod
    def _get_printer(printer_api_key: str):
        """
        Returns a `Printer` if it exists. Otherwise, exception raised.
        """
        printer = Printer.objects.get(pk=printer_api_key)
        return printer
