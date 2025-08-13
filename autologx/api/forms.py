# autologx/api/forms.py
from django import forms
from .models import Vehicle, ServiceRecord

class VehicleForm(forms.ModelForm):
    vin_lookup = forms.CharField(max_length=17, required=False, label="VIN (for auto-lookup)", help_text="Enter VIN to automatically populate vehicle details")

    class Meta:
        model = Vehicle
        fields = ['vin_lookup', 'vin', 'make', 'model', 'year', 'trim', 'engine',
                 'engine_size', 'fuel_type', 'transmission', 'oil_viscosity',
                 'current_mileage', 'stock_tire_size', 'stock_wheel_size',
                 'current_tire_size', 'current_wheel_size']
        widgets = {
            'year': forms.NumberInput(attrs={'min': 1900, 'max': 2030}),
            'engine_size': forms.NumberInput(attrs={'step': '0.1'}),
            'current_mileage': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vin'].required = False

    def clean_vin_lookup(self):
        vin = self.cleaned_data.get('vin_lookup')
        if vin and len(vin) != 17:
            raise forms.ValidationError("VIN must be 17 characters long.")
        return vin.upper() if vin else vin # Normalize to uppercase

class ServiceRecordForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ['service_type', 'date', 'mileage', 'description', 'cost',
                 'shop_name', 'notes', 'next_service_date', 'next_service_mileage']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'next_service_date': forms.DateInput(attrs={'type': 'date'}),
            'mileage': forms.NumberInput(attrs={'min': 0}),
            'cost': forms.NumberInput(attrs={'step': '0.01', 'min': 0}),
            'next_service_mileage': forms.NumberInput(attrs={'min': 0}),
        }
