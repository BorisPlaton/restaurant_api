from django.db import models

from restaurant.utils.models import generate_unique_api_key, generate_pdf_file_path


class CheckType(models.TextChoices):
    kitchen = 'kitchen'
    client = 'client'


class CheckStatus(models.TextChoices):
    NEW = 'new'
    RENDERED = 'rendered'
    PRINTED = 'printed'


class Printer(models.Model):
    """The specific point's printer."""

    api_key = models.CharField(
        "Ключ принтера", unique=True, primary_key=True, db_index=True,
        default=generate_unique_api_key, max_length=32
    )
    check_type = models.CharField("Тип чека", choices=CheckType.choices, max_length=32)
    name = models.CharField("Название принтера", max_length=32)
    point_id = models.PositiveIntegerField("Точка ресторана")

    class Meta:
        ordering = ["point_id"]
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'
        constraints = [
            models.CheckConstraint(
                name='check_type_has_valid_value',
                check=models.Q(check_type__in=CheckType.values),
            )
        ]

    def __str__(self):
        return self.name


class Check(models.Model):
    """Check with order information."""

    order = models.JSONField("Подробности заказа")
    pdf_file = models.FileField("PDF-файл чека", upload_to=generate_pdf_file_path, null=True, blank=True)
    type = models.CharField("Тип чека", choices=CheckType.choices, max_length=32)
    status = models.CharField("Статус чека", choices=CheckStatus.choices, max_length=32)
    printer_id = models.ForeignKey(Printer, models.CASCADE, "checks", verbose_name="Принтер")

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
        constraints = [
            models.CheckConstraint(
                name='type_has_valid_value',
                check=models.Q(type__in=CheckType.values),
            ),
            models.CheckConstraint(
                name='status_has_valid_value',
                check=models.Q(status__in=CheckStatus.values),
            )
        ]

    def __str__(self):
        return f'{self.pk} {self.type}'
