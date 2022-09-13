from rest_framework.request import Request


class RequestDataValidator:
    serializer = None

    def get_request_data(self, request: Request):
        """
        Tries to deserialize the request data and returns it. Otherwise,
        rises exception.
        """
        client_order = self.serializer(data=request.data)
        client_order.is_valid(raise_exception=True)
        return client_order.data
