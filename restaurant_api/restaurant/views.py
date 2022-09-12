from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurant.serializers import Order


class CreateChecks(APIView):
    """
    Accepts a JSON from request body and creates a check
    if it is possible.
    """

    def get_client_order(self) -> Order.data:
        """
        Validates and returns the requested data can. Otherwise,
        raises an exception.
        """
        client_order = Order(data=self.request.data)
        if not client_order.is_valid():
            raise ParseError(client_order.errors)
        return client_order.data

    def post(self, request: Request):
        client_order = self.get_client_order()
        return Response(client_order)


class NewChecks(APIView):
    pass


class CheckFile(APIView):
    pass
