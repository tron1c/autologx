# AutoLogX/autologx/api/services.py
import requests
import logging

# Configure logger for this module
logger = logging.getLogger(__name__)

def decode_vin(vin):
    """
    Decode VIN using NHTSA API
    Returns a dictionary with vehicle information or None if failed
    """
    try:
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('Results'):
            vehicle_data = {}
            for item in data['Results']:
                variable_name = item.get('Variable')
                value = item.get('Value')
                if not value: continue
                if variable_name == 'Make': vehicle_data['make'] = value
                elif variable_name == 'Model': vehicle_data['model'] = value
                elif variable_name == 'Model Year':
                    vehicle_data['year'] = int(value) if value.isdigit() else None
                elif variable_name == 'Trim': vehicle_data['trim'] = value
                elif variable_name == 'Engine Number 1': vehicle_data['engine'] = value
                elif variable_name == 'Engine displacement (cubic inches)':
                    try:
                        cubic_inches = float(value)
                        liters = round(cubic_inches * 0.0163871, 1)
                        vehicle_data['engine_size'] = liters
                    except (ValueError, TypeError): pass
                elif variable_name == 'Fuel Type - Primary': vehicle_data['fuel_type'] = value
                elif variable_name == 'Transmission Style':
                    if 'automatic' in value.lower(): vehicle_data['transmission'] = 'automatic'
                    elif 'manual' in value.lower(): vehicle_data['transmission'] = 'manual'
                    elif 'cvt' in value.lower(): vehicle_data['transmission'] = 'cvt'
                    else: vehicle_data['transmission'] = 'other'
            return vehicle_data
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"VIN Decode Network Error for {vin}: {e}")
        return None
    except Exception as e:
        logger.error(f"VIN Decode Unexpected Error for {vin}: {e}")
        return None
