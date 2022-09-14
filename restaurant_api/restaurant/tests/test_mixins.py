from django.test import TestCase
from rest_framework.exceptions import ValidationError

from restaurant.mixins import DataValidatorMixin
from restaurant.serializers import Order, Client


class TestRequestDataValidator(TestCase):

    def setUp(self):
        self.request_validator = DataValidatorMixin()

    def test_validation_fails_with_invalid_data(self):
        self.request_validator.serializer = Order

        with self.assertRaises(ValidationError):
            self.request_validator.validate_request_data({'wrong': 'data'})

    def test_validation_pass_with_correct_data(self):
        self.request_validator.serializer = Client
        request_data = {'name': 'user', 'phone': 1}
        serializer_data = Client(data=request_data)
        serializer_data.is_valid()
        self.assertEqual(
            self.request_validator.validate_request_data({'name': 'user', 'phone': 1}).data,
            serializer_data.data
        )
