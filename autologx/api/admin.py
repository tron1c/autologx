# autologx/api/admin.py
from django.contrib import admin
from .models import Vehicle, ServiceRecord, Attachment

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('year', 'make', 'model', 'vin', 'user', 'created_at')
    list_filter = ('year', 'make', 'created_at')
    search_fields = ('vin', 'make', 'model', 'user__username')

@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'vehicle', 'date', 'mileage', 'cost')
    list_filter = ('service_type', 'date', 'vehicle__make')
    search_fields = ('description', 'vehicle__vin', 'shop_name')
    date_hierarchy = 'date'

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'attachment_type', 'service_record', 'uploaded_at')
    list_filter = ('attachment_type', 'uploaded_at')
    search_fields = ('title', 'service_record__description')
