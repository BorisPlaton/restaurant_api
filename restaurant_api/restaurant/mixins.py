class DataValidatorMixin:
    """
    Validates incoming data via `serializer` which must
    be a type `rest_framework.serializers.Serializer`.
    """
    serializer = None

    def validate_request_data(self, request_data: dict):
        """
        Validates the data via `serializer` and returns the initialized
        `serializer` with it. Otherwise, rises exception.
        """
        client_order = self.serializer(data=request_data)
        client_order.is_valid(raise_exception=True)
        return client_order
