from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurant.mixins import DataValidatorMixin
from restaurant.serializers import Order
from restaurant.services.commands import create_new_order_and_generate_checks


class CreateChecks(APIView, DataValidatorMixin):
    """
    Accepts a JSON from request body and creates an order check
    if it is possible.
    """

    serializer = Order

    def post(self, request: Request):
        """Accepts the user's order and processes it."""
        client_order = self.validate_request_data(request.data)
        create_new_order_and_generate_checks(client_order)
        return Response({'ok': "Чеки успешно созданы"})


class NewChecks(APIView):
    pass


class CheckFile(APIView):
    pass
