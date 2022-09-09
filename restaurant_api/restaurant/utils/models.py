import uuid


def generate_unique_api_key() -> str:
    """Генерирует уникальное значение ключа для модели `Printer`."""
    return uuid.uuid4().hex


def generate_pdf_file_path(instance, filename: str | None) -> str:
    """
    Возвращает имя pdf-файла (чека) в директории `pdf/` по шаблону
    `<ID заказа>_<тип чека>.pdf`
    """
    return 'pdf/{}_{}.pdf'.format(instance.pk, instance.type)
