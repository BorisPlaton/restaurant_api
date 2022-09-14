import shutil

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db.models import Count
from django.test import TestCase

from config.settings import BASE_DIR
from restaurant.models import Printer, Check


class TestPrinterModel(TestCase):

    @property
    def printer_model(self):
        return Printer

    def test_create_record_without_api_key(self):
        printer = self.printer_model.objects.create(
            check_type='kitchen',
            name='Kitchen printer',
            point_id=12
        )
        self.assertTrue(printer)
        self.assertTrue(isinstance(printer.name, str))
        self.assertTrue(isinstance(printer.point_id, int))
        self.assertTrue(isinstance(printer.api_key, str))
        self.assertFalse(getattr(printer, 'id', False))

    def test_create_record_with_api_key(self):
        printer = self.printer_model.objects.create(
            check_type='kitchen',
            name='Kitchen printer',
            point_id=12,
            api_key='12345qwerty'
        )
        self.assertEqual(printer.pk, printer.api_key)
        self.assertTrue(printer)
        self.assertTrue(isinstance(printer.name, str))
        self.assertTrue(isinstance(printer.point_id, int))
        self.assertTrue(isinstance(printer.api_key, str))

    def test_all_records_has_unique_api_key(self):
        printers_amount = 100
        for i in range(1, printers_amount):
            self.printer_model.objects.create(
                check_type='kitchen',
                name='Kitchen printer',
                point_id=i,
            )
        unique_printers = self.printer_model.objects.all().aggregate(
            unique_printer_amounts=Count('api_key', distinct=True)
        )
        self.assertEqual(unique_printers['unique_printer_amounts'], printers_amount - 1)

    def test_printer_accepts_only_two_types_of_check_type(self):
        with self.assertRaises(ValidationError):
            wrong_printer = self.printer_model(
                check_type='wrong value',
                name='Printer name',
                point_id=2,
            )
            wrong_printer.save()
        with self.assertRaises(ValidationError):
            self.printer_model.objects.create(
                check_type='wrong value',
                name='Printer name',
                point_id=2,
            )
        kitchen_type = self.printer_model.objects.create(
            check_type='kitchen',
            name='Printer name',
            point_id=2,
        )
        client_type = self.printer_model.objects.create(
            check_type='client',
            name='Printer name',
            point_id=2,
        )
        self.assertTrue(kitchen_type)
        self.assertTrue(client_type)

    def test_str_func_returns_model_name_fields(self):
        new_printer = self.printer_model.objects.create(
            check_type='client',
            point_id=1,
            name='name',
        )
        self.assertEqual(str(new_printer), new_printer.name)


class CheckModel(TestCase):

    @property
    def check_model(self):
        return Check

    @staticmethod
    def get_printer_model() -> Printer:
        return Printer.objects.create(
            check_type='client',
            name='client printer',
            point_id=1,
        )

    def test_check_accepts_only_two_types_of_check_type(self):
        printer = self.get_printer_model()
        with self.assertRaises(ValidationError):
            check = self.check_model(
                order={'field': 'value'},
                type='wrong type',
                status='new',
                printer_id=printer
            )
            check.save()
        with self.assertRaises(ValidationError):
            self.check_model.objects.create(
                order={'field': 'value'},
                type='wrong type',
                status='new',
                printer_id=printer
            )
        kitchen_type = self.check_model.objects.create(
            order={'field': 'value'},
            type='kitchen',
            status='new',
            printer_id=printer
        )
        client_type = self.check_model.objects.create(
            order={'field': 'value'},
            type='client',
            status='new',
            printer_id=printer
        )
        self.assertTrue(kitchen_type)
        self.assertTrue(client_type)

    def test_printer_accepts_only_two_types_of_check_type(self):
        printer = self.get_printer_model()
        for i in range(3):
            with self.assertRaises(ValidationError):
                wrong_printer = self.check_model(
                    order={'field': 'value'},
                    type='kitchen',
                    status=str(i),
                    printer_id=printer
                )
                wrong_printer.save()
            with self.assertRaises(ValidationError):
                self.check_model.objects.create(
                    order={'field': 'value'},
                    type='client',
                    status=str(i),
                    printer_id=printer
                )
        new_check = self.check_model.objects.create(
            order={'field': 'value'},
            type='kitchen',
            status='new',
            printer_id=printer
        )
        rendered_check = self.check_model.objects.create(
            order={'field': 'value'},
            type='client',
            status='rendered',
            printer_id=printer
        )
        printed_check = self.check_model.objects.create(
            order={'field': 'value'},
            type='client',
            status='printed',
            printer_id=printer
        )
        self.assertTrue(new_check)
        self.assertTrue(rendered_check)
        self.assertTrue(printed_check)

    def test_str_func_returns_check_type_and_pk(self):
        check_model = self.check_model.objects.create(
            order={'field': 'value'},
            type='client',
            status='printed',
            printer_id=self.get_printer_model()
        )
        return self.assertEqual(
            str(check_model),
            f'{check_model.pk} {check_model.type}'
        )

    def test_saving_pdf_file(self):
        check_model: Check = self.check_model.objects.create(
            order={'field': 'value'},
            type='client',
            status='printed',
            printer_id=self.get_printer_model()
        )
        new_media_root = BASE_DIR / 'test_media'
        try:
            with self.settings(MEDIA_ROOT=new_media_root):
                check_model.pdf_file.save(
                    'file_name.pdf',
                    ContentFile('some pdf stuff..')
                )
                check_model.save()
                self.assertTrue(
                    f'/pdf/{check_model.pk}_{check_model.type}.pdf' in
                    check_model.pdf_file.url
                )
        finally:
            shutil.rmtree(new_media_root)
