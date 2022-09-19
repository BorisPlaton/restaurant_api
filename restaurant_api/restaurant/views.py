from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurant.mixins import RequestResponseSerializer
from restaurant.serializers import Order, CheckSerializer
from restaurant.services.command_invokers import create_new_order_and_generate_checks
from restaurant.services.commands.get_and_mark_check import GetRenderedCheck
from restaurant.services.commands.get_rendered_checks import GetRenderedChecks


class CreateChecks(APIView, RequestResponseSerializer):
    """
    Accepts a JSON from request and creates an order check
    if it is possible.
    """

    request_serializer = Order

    def post(self, request: Request):
        """Receives user's order and processes it."""
        client_order = self.get_request_data(request.data)
        create_new_order_and_generate_checks(client_order)
        return Response({"ok": "Чеки успешно созданы"})


class NewChecks(APIView, RequestResponseSerializer):
    """
    Returns a list of rendered checks' ids.
    """

    def get(self, request: Request):
        """
        Accepts printer's api key and returns ids for
        already rendered checks.
        """
        printer_api_key = self.get_request_parameter_or_400(request.query_params, 'api_key')
        rendered_checks = GetRenderedChecks().execute(printer_api_key)
        return Response({"checks": CheckSerializer(rendered_checks, many=True).data})


class CheckFile(APIView, RequestResponseSerializer):
    """
    Returns check's PDF-file.
    """

    def get(self, request: Request):
        """
        Accepts printer's api key, check's id and returns
        a PDF-file of the check.
        """
        printer_api_key = self.get_request_parameter_or_400(request.query_params, 'api_key')
        check_id = self.get_request_parameter_or_400(request.query_params, 'check_id')
        check_pdf_file = GetRenderedCheck().execute(printer_api_key, check_id)
        return HttpResponse(check_pdf_file, content_type='application/pdf')
