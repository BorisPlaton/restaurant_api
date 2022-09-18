from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase
from rq import Queue

from restaurant.services.commands.enqueue_checks_generation import EnqueueChecksGeneration


class TestEnqueueChecksGenerationService(TestCase):

    @property
    def service(self):
        return EnqueueChecksGeneration()

    def test_service_uses_wkhtmltopdf_queue(self):
        self.assertEqual(self.service.queue.name, 'wkhtmltopdf')
        self.assertTrue(isinstance(self.service.queue, Queue))

    @mock.patch('restaurant.services.commands.enqueue_checks_generation.Queue')
    @mock.patch('restaurant.services.commands.enqueue_checks_generation.django_rq')
    def test_enqueue_pdf_generation_creates_jobs_for_every_check_instance(
            self, rq_mock, queue_mock
    ):
        check_jobs = []
        check_ids = [1, 2, 3, 4, 5, 6]

        def add_id_to_check_jobs(*args, **kwargs):
            check_jobs.append(*kwargs.pop('args'))

        queue_mock.prepare_data = MagicMock(side_effect=add_id_to_check_jobs)
        rq_mock.get_queue.return_value = MagicMock()

        self.service._enqueue_checks_ids_for_generating_pdf(check_ids)
        self.assertEqual(len(check_jobs), len(check_ids))

    @mock.patch('restaurant.services.commands.enqueue_checks_generation.Queue')
    @mock.patch('restaurant.services.commands.enqueue_checks_generation.django_rq')
    def test_enqueue_pdf_generation_creates_jobs_without_id_duplication(
            self, rq_mock, queue_mock
    ):
        check_jobs = []
        check_ids = [1, 1, 1, 1, 1, 1, ]

        def add_id_to_check_jobs(*args, **kwargs):
            check_jobs.append(*kwargs.pop('args'))

        queue_mock.prepare_data = MagicMock(side_effect=add_id_to_check_jobs)
        rq_mock.get_queue.return_value = MagicMock()

        self.service._enqueue_checks_ids_for_generating_pdf(check_ids)
        self.assertEqual(len(check_jobs), 1)
