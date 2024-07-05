# aemo_to_tariff/energex.py
from datetime import datetime
from pytz import timezone

def time_zone():
    return 'Australia/Brisbane'

NOUS = (0.02840, 0.15936, 0.03513)

def daily():
    return 32.757 + 15.500

def peak_hours():
    # Peak Energy 4pm-9pm every day
    return [16, 17, 18, 19, 20]

def peak_cost():
    return 15.936

def off_peak_hours():
    # Off-peak Energy 9pm-4pm every day
    return [10, 11, 12, 13, 14, 15]

def off_peak_cost():
    return 2.840

def shoulder_hours():
    # Not peak or off-peak
    return [21, 22, 23, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def shoulder_cost():
    return 3.513

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
    if tariff == '6970':
        if hour in peak_hours():
            price_c_kwh = peak_cost()
        elif hour in shoulder_hours():
            price_c_kwh = shoulder_cost()
        elif hour in off_peak_hours():
            price_c_kwh = off_peak_cost()
        else:
            price_c_kwh = off_peak_cost()
        price_c_kwh += rrp_c_kwh
    else:
        # Terrible approximation
        slope = 1.037869032618134
        intecept = 5.586606750833143
        return rrp_c_kwh * slope + intecept
    
    return price_c_kwh + rrp_c_kwh
