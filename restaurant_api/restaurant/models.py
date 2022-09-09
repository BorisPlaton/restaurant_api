from django.db import models

from restaurant.utils.models import generate_unique_api_key, generate_pdf_file_path
from restaurant.validators import ChoicesValidator


CHECK_TYPE_CHOICES = [
    ('kitchen', 'Kitchen'),
    ('client', 'Client'),
]


class Printer(models.Model):
    """Принтер определенной точки сети ресторанов."""

    api_key = models.CharField(
        "Ключ принтера", unique=True, primary_key=True, db_index=True,
        default=generate_unique_api_key, max_length=32
    )
    check_type = models.CharField(
        "Тип чека", choices=CHECK_TYPE_CHOICES, max_length=32,
        validators=[ChoicesValidator(CHECK_TYPE_CHOICES)]
    )
    name = models.CharField("Название принтера", max_length=32)
    point_id = models.PositiveIntegerField("Точка ресторана")

    class Meta:
        ordering = ["point_id"]
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'

    def __str__(self):
        return self.name


class Check(models.Model):
    """Чек с информацией о заказе."""

    class CheckStatus(models.TextChoices):
        NEW = 'new'
        RENDERED = 'rendered'
        PRINTED = 'printed'

    order = models.JSONField("Подробности заказа")
    pdf_file = models.FileField("PDF-файл чека", upload_to=generate_pdf_file_path, null=True, blank=True)
    type = models.CharField(
        "Тип чека", choices=CHECK_TYPE_CHOICES, max_length=32,
        validators=[ChoicesValidator(CHECK_TYPE_CHOICES)]
    )
    status = models.CharField(
        "Статус чека", choices=CheckStatus.choices, max_length=32,
        validators=[ChoicesValidator(CheckStatus.choices)]
    )

    printer_id = models.ForeignKey(Printer, models.CASCADE, "checks", verbose_name="Принтер")

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self):
        return '{} {}'.format(self.pk, self.type)
