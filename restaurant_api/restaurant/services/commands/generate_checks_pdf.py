import base64
import json
import os

import requests
from django.core.files.base import ContentFile
from django.template.loader import render_to_string

from restaurant.models import Check, CheckStatus
from restaurant.services.commands.abstract import BaseCommand


class GenerateChecksPDF(BaseCommand):
    """
    Generates PDF-files for `Check` instances. In the end marks the
    instances as `rendered`.
    """

    @classmethod
    def execute(cls, check_id: int):
        """
        Creates a PDF-file for the `Check` instance which `id` field matches
        the `check_id` value.
        """
        check_pdf = cls._generate_check_pdf(check_id)
        cls._set_pdf_file_to_check_instance(check_id, check_pdf)
        return cls._mark_check_as_rendered(check_id)

    @classmethod
    def _generate_check_pdf(cls, check_id: int):
        """Generates a PDF-file for `Check` model and returns it."""
        html_file_to_render = cls._get_check_html(check_id)
        return cls._convert_html_to_pdf(html_file_to_render)

    @staticmethod
    def _set_pdf_file_to_check_instance(check_id: int, pdf_file: bytes):
        """Sets the given PDF-file to the `Check` instance. """
        Check.objects.get(pk=check_id).pdf_file.save(
            'PDF-file',
            ContentFile(pdf_file)
        )

    @staticmethod
    def _mark_check_as_rendered(check_id: int):
        """
        Marks the check which `id` field matches the `check_id` value as rendered.
        """
        Check.objects.filter(pk=check_id).update(status=CheckStatus.RENDERED)

    @staticmethod
    def _get_check_html(check_id: int) -> str:
        """
        Renders the corresponding(kitchen or client) HTML-file with order data
        and returns it.
        """
        client_order = Check.objects.values('order', 'type').get(pk=check_id)
        return render_to_string(f'restaurant/{client_order["type"]}_check.html', client_order['order'])

    @staticmethod
    def _convert_html_to_pdf(html_file: str) -> bytes:
        """
        Converts the HTML-file to PDF using the `wkhtmltopdf` docker image.
        Returns the result as bytes.
        """
        url = f"http://localhost:{os.getenv('TO_PDF_PORT')}/"
        data = {
            'contents': base64.b64encode(html_file.encode()).decode(),
        }
        headers = {
            'Content-Type': 'application/json',
        }
        a = json.dumps(data)
        response = requests.post(
            url, data=a,
            headers=headers
        )
        return response.content
