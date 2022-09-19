from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidRequestData(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Вы отправили некорректные данные."


class CheckAlreadyCreated(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Для данного заказа уже созданы чеки."


class CheckNotCreated(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Данного чека не существует."


class PointHasNoPrinters(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Для данной точки не настроено ни одного принтера."


class QueryParameterNotSpecified(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Вы не указали параметр."


class WrongPrinterApiKey(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Ошибка авторизации."


class CheckDoesNotHavePDF(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Для данного чека не сгенерирован PDF-файл"
