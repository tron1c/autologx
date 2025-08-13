# AutoLogX/autologx/api/forms.py
from django import forms
from .models import Vehicle, ServiceRecord

# --- Define a custom widget for multiple file uploads ---
# Override the 'allow_multiple_selected' attribute
class MultipleFileInput(forms.FileInput):
    """Custom FileInput widget that explicitly allows the 'multiple' attribute."""
    # This is the key change: Tell Django this widget handles multiple files
    allow_multiple_selected = True

# Custom field using the custom widget
class MultipleFileField(forms.FileField):
    """Custom FileField that uses the MultipleFileInput widget."""
    # Set the custom widget
    widget = MultipleFileInput

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # Handle cleaning for single or multiple files
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            # If multiple files are uploaded, clean each one
            result = [single_file_clean(d, initial) for d in data]
        else:
            # If a single file is uploaded, clean it normally
            result = single_file_clean(data, initial)
        return result
# --- End of custom widget/field definition ---

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
    # Add a field for file attachments using the custom field/widget
    attachments = MultipleFileField(
        label="Attach Files (Receipts, Photos, etc.)",
        required=False,
        help_text="Select one or more files (PDF, JPG, PNG, etc.)."
    )

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

    # Optional: Add validation for file types/sizes if needed in the future
    # def clean_attachments(self):
    #     attachments = self.cleaned_data.get('attachments', [])
    #     if attachments:
    #         for attachment in attachments:
    #             # Example validation: Check file extension
    #             # valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    #             # ext = os.path.splitext(attachment.name)[1].lower()
    #             # if ext not in valid_extensions:
    #             #     raise forms.ValidationError(f"File type '{ext}' is not supported. Only PDF, JPG, and PNG files are allowed.")
    #             # Example validation: Check file size (e.g., 5MB max)
    #             # if attachment.size > 5 * 1024 * 1024:
    #             #     raise forms.ValidationError(f"File '{attachment.name}' is too large. Maximum size is 5MB.")
    #     return attachments
