# Generated by Django 4.1.1 on 2022-09-09 19:09

from django.db import migrations, models
import django.db.models.deletion
import restaurant.utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('api_key', models.CharField(db_index=True, default=restaurant.utils.models.generate_unique_api_key, max_length=32, primary_key=True, serialize=False, unique=True, verbose_name='Ключ принтера')),
                ('name', models.CharField(max_length=32, verbose_name='Название принтера')),
                ('check_type', models.CharField(choices=[('kitchen', 'Kitchen'), ('client', 'Client')], max_length=32, verbose_name='Тип чека')),
                ('point_id', models.PositiveIntegerField(verbose_name='Точка ресторана')),
            ],
            options={
                'verbose_name': 'Принтер',
                'verbose_name_plural': 'Принтеры',
                'ordering': ['point_id'],
            },
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('kitchen', 'Kitchen'), ('client', 'Client')], max_length=32, verbose_name='Тип чека')),
                ('status', models.CharField(choices=[('new', 'New'), ('rendered', 'Rendered'), ('printed', 'Printed')], max_length=32, verbose_name='Статус чека')),
                ('order', models.JSONField(verbose_name='Подробности заказа')),
                ('pdf_file', models.FileField(upload_to='', verbose_name='PDF-файл чека')),
                ('printer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='restaurant.printer', verbose_name='Принтер')),
            ],
            options={
                'verbose_name': 'Чек',
                'verbose_name_plural': 'Чеки',
            },
        ),
    ]
