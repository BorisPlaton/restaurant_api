import json
import os

import django_rq
import requests
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from rq import Queue

from restaurant.models import Check, CheckStatus


class GenerateChecksPdf:
    """Generates PDF files for `Check` instance in the background."""

    def execute(self, checks_ids: list[int]):
        """Execute pdf generation command for checks."""
        self._enqueue_checks_ids_for_generating_pdf(checks_ids)

    def _enqueue_checks_ids_for_generating_pdf(self, checks_ids: list[int]):
        """Enqueue new jobs for workers."""
        self.queue.enqueue_many(
            [Queue.prepare_data(self._create_pdf_for_check, check_id) for check_id in checks_ids]
        )

    def _create_pdf_for_check(self, check_id: int):
        """
        Creates pdf for the `Check` instance which `id` field matches the `check_id` value.
        """
        check_pdf = self._generate_check_pdf(check_id)
        self._set_pdf_file_to_check_instance(check_id, check_pdf)
        self._mark_check_is_rendered(check_id)

    def _generate_check_pdf(self, check_id: int) -> bytes:
        """Generates a pdf file for the `Check` model and returns it."""
        html_file_to_render = self._get_check_html(check_id)
        return self._convert_html_to_pdf(html_file_to_render)

    @staticmethod
    def _set_pdf_file_to_check_instance(check_id: int, pdf_file: bytes):
        """Sets the given pdf file to the `Check` instance. """
        Check.objects.get(pk=check_id).pdf_file.save(
            'check pdf file',
            ContentFile(pdf_file)
        )

    @staticmethod
    def _convert_html_to_pdf(html_file: str) -> bytes:
        """
        Converts the html file to pdf using the `wkhtmltopdf` docker image.
        Returns a result.
        """
        url = f"http://localhost:{os.getenv('TO_PDF_PORT')}/"
        data = {
            'contents': html_file.encode('base64'),
        }
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response.content

    @staticmethod
    def _mark_check_is_rendered(check_id: int):
        """
        Marks the check which `id` field matches the `check_id` value as rendered.
        """
        Check.objects.filter(pk=check_id).update(status=CheckStatus.RENDERED)

    @staticmethod
    def _get_check_html(check_id: int) -> str:
        """
        Renders the corresponding(kitchen or client) html file with the order data
        and returns it.
        """
        client_order: Check = Check.objects.filter(pk=check_id).values('order', 'type')
        return render_to_string(
            f'restaurant/{client_order.type}_check.html', client_order.order
        )

    def __init__(self):
        """Gets a queue which stores all the jobs to be done."""
        self.queue = django_rq.get_queue('wkhtmltopdf')
