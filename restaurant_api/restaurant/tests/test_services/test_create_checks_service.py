from django.test import TestCase

from restaurant.exceptions.exceptions import PointHasNoPrinters, CheckAlreadyCreated
from restaurant.models import Printer, Check
from restaurant.services.commands.create_order_checks import CreateOrderChecks


class TestCreateOrderChecksService(TestCase):
    fixtures = ['tests/test_printer_fixture.json']

    @property
    def service(self):
        return CreateOrderChecks()

    @property
    def client_order(self):
        return {'id': 1, 'items': [1, 2, 3, 4]}

    def test_exception_raises_if_point_doesnt_have_printers(self):
        with self.assertRaises(PointHasNoPrinters):
            self.service._get_all_printers_at_point(12345)

    def test_exception_raises_if_order_is_already_added_to_db(self):
        printer = Printer.objects.first()
        Check.objects.create(
            order=self.client_order,
            type=printer.check_type,
            status='new',
            printer_id=printer
        )
        with self.assertRaises(CheckAlreadyCreated):
            self.service._check_order_is_new(self.client_order['id'])

    def test_all_returned_points_printers_is_correct(self):
        printers_at_point = Printer.objects.filter(point_id=4)
        printers_at_point_via_service = self.service._get_all_printers_at_point(4)
        self.assertQuerysetEqual(printers_at_point, printers_at_point_via_service)

    def test_true_is_returned_if_order_doesnt_exist_in_db(self):
        self.assertTrue(self.service._check_order_is_new(5))

    def test_new_checks_records_amount_for_printers(self):
        client_data = {
            "id": 123456,
            "price": 780,
            "items": [
                {
                    "name": "Вкусная пицца",
                    "quantity": 2,
                    "unit_price": 250
                },
                {
                    "name": "Не менее вкусные роллы",
                    "quantity": 1,
                    "unit_price": 280
                }
            ],
            "address": "г. Уфа, ул. Ленина, д. 42",
            "client": {
                "name": "Иван",
                "phone": 9173332222
            },
            "point_id": 1
        }
        self.assertEqual(len(self.service.execute(client_data)), 2)
