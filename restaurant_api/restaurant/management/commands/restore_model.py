from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Restore the model which name matches the provided one'

    def add_arguments(self, parser):
        parser.add_argument(
            'model_name',
            help='The model to restore.'
        )

    def handle(self, *args, **options):
        table = ContentType.objects.get(app_label='restaurant', model=options['model_name'])
        result = str(table.model_class().objects.all().delete())
        self.stdout.write(result)
