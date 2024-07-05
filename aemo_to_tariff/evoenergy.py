# aemo_to_tariff/evoenergy.py
from datetime import datetime
from pytz import timezone

def time_zone():
    return 'Australia/ACT'

def daily():
    return 32.757 + 15.500

def peak_hours():
    # Peak Energy 7am-9am and 5pm-9pm every day
    return [7, 8, 17, 18, 19, 20]

def peak_cost():
    return 14.109

def solar_soak_hours():
    # Solar Soak Energy 11am-3pm every day
    return [11, 12, 13, 14]

def solar_soak_cost():
    return 1.757

def off_peak_hours():
    # Off-peak Energy 9pm-7am, 9am-11am and 3pm-5pm every day
    return [21, 22, 23, 9, 10, 15, 16]

def off_peak_cost():
    return 3.918

def convert(interval_time: datetime, tariff: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for Evoenergy.
    
    Parameters:
    - interval_time (str): The interval time.
    - tariff (str): The tariff code.
    - rrp (float): The Regional Reference Price in $/MWh.
    
    Returns:
    - float: The price in c/kWh.
    """
    interval_time = interval_time.astimezone(timezone(time_zone()))
    hour = interval_time.hour
    rrp_c_kwh = rrp / 10
    if tariff == '017':
        if hour in peak_hours():
            price_c_kwh = peak_cost()
        elif hour in solar_soak_hours():
            price_c_kwh = solar_soak_cost()
        elif hour in off_peak_hours():
            price_c_kwh = off_peak_cost()
        else:
            price_c_kwh = off_peak_cost()
        return price_c_kwh + rrp_c_kwh
    else:
        # Terrible approximation
        slope = 1.037869032618134
        intecept = 5.586606750833143
        return rrp_c_kwh * slope + intecept    
