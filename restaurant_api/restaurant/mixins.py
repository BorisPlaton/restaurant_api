from restaurant.exceptions.exceptions import QueryParameterNotSpecified


class RequestResponseSerializer:
    """
    Validates incoming data via `serializer` which must
    be a type `rest_framework.serializers.Serializer`.
    """
    request_serializer = None

    def get_request_data(self, request_data: dict):
        """
        Validates the data via `request_serializer` and returns the initialized
        `serializer` with it. Otherwise, rises exception.
        """
        client_order = self.request_serializer(data=request_data)
        client_order.is_valid(raise_exception=True)
        return client_order

    def get_request_parameter_or_400(self, request_parameters: dict, parameter_name: str):
        """Returns value of the parameter. Otherwise, raises an error."""
        parameter_value = self.get_request_parameter(request_parameters, parameter_name)
        if not parameter_value:
            raise QueryParameterNotSpecified(
                QueryParameterNotSpecified.default_detail[:-2] +
                " `{}`.".format(parameter_name)
            )
        return parameter_value

    @staticmethod
    def get_request_parameter(request_parameters: dict, parameter_name: str):
        """Returns a value of the parameter. If it doesn't exist, returns `None`."""
        parameter_value = request_parameters.get(parameter_name)
        return parameter_value
