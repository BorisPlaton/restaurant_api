from typing import Iterable

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ChoicesValidator:
    """Проверяет что переданное значение входит в список разрешенных."""

    def __init__(self, choices: Iterable[tuple]):
        """Сохраняет список доступных значений для будущей проверки."""
        self.choices = choices

    def __call__(self, value):
        """Проверяет что `value` входит в список доступных значений."""
        available_values = [choice_value[0] for choice_value in self.choices]
        if value not in available_values:
            raise ValidationError(
                "`{}` не входит в список доступных значений"
                "{}".format(value, available_values)
            )
