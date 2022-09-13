from rest_framework.views import exception_handler


def error_exception_handler(exc, context):
    """
    Changes the `detail` key to `error` and returns
    response.
    """
    response = exception_handler(exc, context)
    if response is not None:
        response.data['error'] = response.data.pop(
            'detail', 'Произошла ошибка при обработке запроса.'
        )
    return response
