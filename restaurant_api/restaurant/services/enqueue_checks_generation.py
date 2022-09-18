import django_rq
from rq import Queue

from restaurant.services.generate_checks_pdf import GenerateChecksPDF


class EnqueueChecksGeneration:
    """
    Enqueues PDF-files generation for `Check` instances in the background.
    """

    def execute(self, checks_ids: list[int]):
        """Execute a PDF-files generation command for checks."""
        return self._enqueue_checks_ids_for_generating_pdf(checks_ids)

    def _enqueue_checks_ids_for_generating_pdf(self, checks_ids: list[int]):
        """
        Enqueue new jobs for `RQ` background workers to execute
        a PDF-files generation.
        """
        jobs_to_enqueue = [
            Queue.prepare_data(GenerateChecksPDF.execute, args=[check_id], result_ttl=0)
            for check_id in set(checks_ids)
        ]
        return self.queue.enqueue_many(jobs_to_enqueue)

    def __init__(self):
        """Gets a queue which stores all jobs to be done."""
        self.queue = django_rq.get_queue('wkhtmltopdf')
