from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

from restaurant.models import Check, CheckStatus
from restaurant.services.commands.generate_checks_pdf import GenerateChecksPDF
from restaurant.tests.utils import rewrite_media_dir


class TestPDFChecksGenerationService(TestCase):
    fixtures = ['tests/test_printer_fixture.json', 'tests/test_check_fixture.json']

    @property
    def service(self):
        return GenerateChecksPDF()

    def test_check_html_file_generation_is_string_type(self):
        check_id = Check.objects.first().pk
        html_file = self.service._get_check_html(check_id)
        self.assertTrue(isinstance(html_file, str))

    def test_check_html_file_is_corresponding_type(self):
        check = Check.objects.get(pk=1)
        html_file = self.service._get_check_html(check.pk)
        self.assertIn("Чек для кухни", html_file)

        second_check = Check.objects.get(pk=2)
        second_html_file = self.service._get_check_html(second_check.pk)
        self.assertIn("Чек для клиента", second_html_file)

    def test_marking_check_models_as_rendered(self):
        check = Check.objects.get(pk=1)
        self.assertEqual(check.status, CheckStatus.NEW)
        self.service._mark_check_as_rendered(check.pk)
        check.refresh_from_db()
        self.assertEqual(check.status, CheckStatus.RENDERED)

    @rewrite_media_dir
    def test_setting_pdf_file_for_check_instance(self):
        check = Check.objects.get(pk=1)
        pdf_file_content = b'It is a pdf file.'
        self.assertFalse(check.pdf_file)
        self.service._set_pdf_file_to_check_instance(check.pk, pdf_file_content)
        check.refresh_from_db()
        with check.pdf_file.open('r') as pdf_file:
            self.assertEqual(pdf_file.read(), pdf_file_content.decode())

    @mock.patch('restaurant.services.commands.generate_checks_pdf.requests')
    def test_convert_to_pdf_returns_bytes(self, requests_mock: MagicMock):
        response_mock = MagicMock(content=b'pdf file')
        requests_mock.post.return_value = response_mock
        pdf_file = self.service._convert_html_to_pdf('html file')
        self.assertEqual(response_mock.content, pdf_file)
