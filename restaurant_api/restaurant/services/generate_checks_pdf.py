import base64
import json
import os
from pathlib import Path

import django_rq
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django import template
from rq import Queue

from restaurant.models import Check, CheckStatus


class GenerateChecksPdf:
    """Generates PDF files for `Check` instance in the background."""

    def execute(self, checks_ids: list[int]):
        """Execute pdf generation command for checks."""
        self._enqueue_checks_ids_for_generating_pdf(checks_ids)

    def _enqueue_checks_ids_for_generating_pdf(self, checks_ids: list[int]):
        """Enqueue new jobs for workers."""
        jobs_to_enqueue = [
            Queue.prepare_data(self._create_pdf_for_check, args=[check_id])
            for check_id in checks_ids
        ]
        self.queue.enqueue_many(jobs_to_enqueue)

    @classmethod
    def _create_pdf_for_check(cls, check_id: int):
        """
        Creates pdf for the `Check` instance which `id` field matches the `check_id` value.
        """
        check_pdf = cls._generate_check_pdf(check_id)
        cls._set_pdf_file_to_check_instance(check_id, check_pdf)
        cls._mark_check_is_rendered(check_id)

    @classmethod
    def _generate_check_pdf(cls, check_id: int) -> bytes:
        """Generates a pdf file for the `Check` model and returns it."""
        html_file_to_render = cls._get_check_html(check_id)
        return cls._convert_html_to_pdf(html_file_to_render)

    @staticmethod
    def _set_pdf_file_to_check_instance(check_id: int, pdf_file: bytes):
        """Sets the given pdf file to the `Check` instance. """
        Check.objects.get(pk=check_id).pdf_file.save(
            'check pdf file',
            ContentFile(pdf_file)
        )

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
        client_order = Check.objects.values('order', 'type').get(pk=check_id)
        return render_to_string(f'restaurant/{client_order["type"]}_check.html', client_order['order'])

    @staticmethod
    def _convert_html_to_pdf(html_file: str) -> bytes:
        """
        Converts the html file to pdf using the `wkhtmltopdf` docker image.
        Returns a result.
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

    def __init__(self):
        """Gets a queue which stores all the jobs to be done."""
        self.queue = django_rq.get_queue('wkhtmltopdf')
