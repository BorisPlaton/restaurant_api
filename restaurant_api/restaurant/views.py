from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurant.mixins import RequestDataValidator
from restaurant.serializers import Order
from restaurant.services.create_order_checks import PointOrderChecks


class CreateChecks(APIView, RequestDataValidator):
    """
    Accepts a JSON from request body and creates an order check
    if it is possible.
    """

    serializer = Order

    def post(self, request: Request):
        client_order = self.get_request_data(request)
        PointOrderChecks().create_checks_for_point(client_order)
        return Response({'ok': "Чеки успешно созданы"})


class NewChecks(APIView):
    pass


class CheckFile(APIView):
    pass
