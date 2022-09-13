from django.db import models

from restaurant.utils.models import generate_unique_api_key, generate_pdf_file_path
from restaurant.validators import ChoicesValidator


CHECK_TYPE_CHOICES = [
    ('kitchen', 'Kitchen'),
    ('client', 'Client'),
]


class BaseModel(models.Model):
    """
    The abstract model has basic, general functionality
    that is reused in children classes.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Ensures validating all fields."""
        self.full_clean()
        return super().save(*args, **kwargs)


class Printer(BaseModel):
    """The specific point's printer."""

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


class Check(BaseModel):
    """Check with order information."""

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
        return f'{self.pk} {self.type}'
