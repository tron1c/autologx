# autologx/api/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import logging
from .models import Vehicle, ServiceRecord
from .forms import VehicleForm, ServiceRecordForm
from .services import decode_vin

# Configure logger for this module
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('vehicle_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(user=request.user)
    return render(request, 'vehicles/list.html', {'vehicles': vehicles})

@login_required
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    service_records = ServiceRecord.objects.filter(vehicle=vehicle).order_by('-date')
    return render(request, 'vehicles/detail.html', {
        'vehicle': vehicle,
        'service_records': service_records
    })

@login_required
@require_http_methods(["GET", "POST"])
def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            if not vehicle.vin and form.cleaned_data.get('vin_lookup'):
                vehicle.vin = form.cleaned_data['vin_lookup']
            vehicle.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('vehicle_detail', pk=vehicle.pk)
    else:
        initial_data = {}
        vin_param = request.GET.get('vin')
        if vin_param: initial_data['vin_lookup'] = vin_param
        form = VehicleForm(initial=initial_data)
    return render(request, 'vehicles/form.html', {'form': form, 'title': 'Add Vehicle'})

@login_required
def vehicle_edit(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('vehicle_detail', pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicles/form.html', {
        'form': form,
        'title': 'Edit Vehicle',
        'vehicle': vehicle
    })

@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('vehicle_list')
    return render(request, 'vehicles/confirm_delete.html', {'vehicle': vehicle})

@login_required
def service_record_create(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk, user=request.user)
    if request.method == 'POST':
        form = ServiceRecordForm(request.POST)
        if form.is_valid():
            service_record = form.save(commit=False)
            service_record.vehicle = vehicle
            service_record.save()
            messages.success(request, 'Service record added successfully!')
            return redirect('vehicle_detail', pk=vehicle.pk)
    else:
        form = ServiceRecordForm()
    return render(request, 'service_records/form.html', {
        'form': form,
        'title': 'Add Service Record',
        'vehicle': vehicle
    })

@login_required
def vin_lookup(request):
    if request.method == 'POST':
        try:
            # Determine how data is sent (JSON or form)
            if request.content_type == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
                vin = data.get('vin', '').strip().upper()
            else: # Assume form data
                vin = request.POST.get('vin', '').strip().upper()
            if not vin:
                logger.warning("VIN lookup attempted with empty VIN.")
                return JsonResponse({'success': False, 'error': 'VIN is required'})
            if len(vin) != 17:
                logger.info(f"VIN lookup attempted with invalid length VIN: {vin}")
                return JsonResponse({'success': False, 'error': 'VIN must be 17 characters long'})
            vehicle_data = decode_vin(vin)
            # --- FIXED SYNTAX ERROR HERE ---
            if vehicle_data: # <--- Corrected condition from 'if vehicle_:'
                logger.info(f"VIN lookup successful for {vin}")
                return JsonResponse({'success': True, 'data': vehicle_data})
            else:
                logger.info(f"VIN lookup failed for {vin} - API returned no data or error.")
                return JsonResponse({'success': False, 'error': 'Could not decode VIN. Please check the VIN and try again.'})
        except json.JSONDecodeError as e:
            logger.error(f"VIN lookup failed due to invalid JSON: {e}")
            return JsonResponse({'success': False, 'error': 'Invalid JSON data received.'})
        except Exception as e:
            # Log the full traceback for debugging (optional)
            import traceback
            logger.error(f"VIN lookup failed with unexpected error: {e}\n{traceback.format_exc()}") # Added newline for clarity
            return JsonResponse({'success': False, 'error': f'An internal error occurred: {str(e)}'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# Ensure there's a newline at the end of the file
