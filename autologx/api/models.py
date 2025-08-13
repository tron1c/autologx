# AutoLogX/autologx/api/models.py
from django.db import models
from django.contrib.auth.models import User
import os

class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    vin = models.CharField(max_length=17, unique=True, blank=True, null=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    trim = models.CharField(max_length=50, blank=True)
    engine = models.CharField(max_length=100, blank=True)
    engine_size = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    fuel_type = models.CharField(max_length=20, blank=True)
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'), ('automatic', 'Automatic'), ('cvt', 'CVT'),
        ('semi_automatic', 'Semi-Automatic'), ('other', 'Other'),
    ]
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, blank=True)
    oil_viscosity = models.CharField(max_length=10, blank=True, help_text="e.g., 0W-20, 5W-30")
    current_mileage = models.IntegerField(default=0)
    last_oil_change_mileage = models.IntegerField(blank=True, null=True)
    last_oil_change_date = models.DateField(blank=True, null=True)
    last_service_mileage = models.IntegerField(blank=True, null=True)
    last_service_date = models.DateField(blank=True, null=True)
    stock_tire_size = models.CharField(max_length=30, blank=True)
    stock_wheel_size = models.CharField(max_length=20, blank=True)
    current_tire_size = models.CharField(max_length=30, blank=True)
    current_wheel_size = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class ServiceRecord(models.Model):
    SERVICE_TYPES = [
        ('oil_change', 'Oil Change'), ('tire_rotation', 'Tire Rotation'),
        ('brake_service', 'Brake Service'), ('engine_repair', 'Engine Repair'),
        ('inspection', 'Inspection'), ('other', 'Other'),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='service_records')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    date = models.DateField()
    mileage = models.IntegerField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    shop_name = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    next_service_date = models.DateField(blank=True, null=True)
    next_service_mileage = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_type} for {self.vehicle} on {self.date}"

def attachment_upload_path(instance, filename):
    return os.path.join('vehicles', str(instance.service_record.vehicle.id), 'service_records', str(instance.service_record.id), filename)

class Attachment(models.Model):
    ATTACHMENT_TYPES = [
        ('receipt', 'Receipt'), ('invoice', 'Invoice'), ('photo', 'Photo'),
        ('warranty', 'Warranty'), ('manual', 'Manual'), ('other', 'Other'),
    ]
    service_record = models.ForeignKey(ServiceRecord, on_delete=models.CASCADE, related_name='attachments')
    title = models.CharField(max_length=200)
    attachment_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPES)
    file = models.FileField(upload_to=attachment_upload_path) # Requires Pillow
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.attachment_type}) for SR {self.service_record.id}"
