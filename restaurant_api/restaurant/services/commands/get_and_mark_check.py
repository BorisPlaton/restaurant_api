from django.db.models import QuerySet

from restaurant.exceptions.exceptions import CheckNotCreated, CheckDoesNotHavePDF
from restaurant.models import Check, CheckStatus
from restaurant.services.commands.abstract import BaseCommand
from restaurant.services.commands.get_rendered_checks import GetRenderedChecks


class GetRenderedCheck(BaseCommand):
    """
    Returns a PDF-file of check and marks the check as
    printed.
    """

    def execute(self, printer_api_key: str, check_id: int):
        """
        Accepts a printer api key to verify if the printer exists and
        a check id which pdf file will be returned.
        """
        rendered_checks = GetRenderedChecks().execute(printer_api_key)
        concrete_rendered_check = self._get_rendered_check(rendered_checks, check_id)
        self._mark_check_as_printed(concrete_rendered_check)
        return self._get_check_pdf_file(concrete_rendered_check)

    @staticmethod
    def _get_rendered_check(rendered_checks: QuerySet[Check], check_id: int) -> Check:
        """Returns a specific check instance from already rendered checks."""
        check = rendered_checks.filter(pk=check_id)
        if not check.exists():
            raise CheckNotCreated
        check_instance = check.first()
        if check_instance.status != CheckStatus.RENDERED:
            raise CheckDoesNotHavePDF
        return check_instance

    @staticmethod
    def _mark_check_as_printed(check: Check):
        """Marks the check as printed."""
        check.status = CheckStatus.PRINTED
        check.save()
        return check

    @staticmethod
    def _get_check_pdf_file(check: Check) -> bytes:
        """Returns content of check pdf file."""
        with check.pdf_file.open('rb') as f:
            return f.read()
