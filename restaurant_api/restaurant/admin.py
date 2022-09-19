from django.contrib import admin

from restaurant.models import Printer, Check


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ['api_key', 'name', 'check_type']
    readonly_fields = ['api_key']
    list_display_links = ['name', 'api_key']
    list_filter = ['check_type']


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'status', 'printer_id']
    list_filter = ['type', 'status', 'printer_id']
